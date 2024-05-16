import os
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import *
from datetime import datetime
from .scripts import *
from jsonschema import validate
from django.contrib import messages
import json
from django.db.models import Q
from wsgiref.util import FileWrapper
import mimetypes
from django.core.paginator import Paginator




#Upload Json File to Create HTML Forms
class JsonFormConfiguration(View):
	def __init__(self,*args,**kwargs):
		self.data= JsonConfiguration.objects.filter(form_name="JSON Configuration form").first()

		path = os.getcwd()

		self.queryset = self.data.file.read()

	def get(self,request,*args, **kwargs):
		
		file = self.queryset 
		# print(file, "file")
		queryset_dict = json.loads(file)
		print(queryset_dict, "queryset_dict")

		action = request.GET.get('action',None)
		instance_id = request.GET.get('id',None)
		search = request.GET.get('search',None)
		entries = request.GET.get('entries', '5')

		if action == 'create':

			context = {
			"JsonForm": queryset_dict,
			"redirect":"json-config"
			}       
			return render(request, 'create_configuration.html', context)

		elif action == 'edit':
			if instance_id:
				user_data = JsonConfiguration.objects.filter(status_code=1).get(id=instance_id)
				
				json_string = str(queryset_dict)

				context = { 
					"data":user_data, 
					"JsonForm": queryset_dict, 
					"json_string":queryset_dict, 
					"redirect":"json-config"
				}

				return render(request,'edit_configuration.html',context)

		elif action == 'delete':
			if instance_id:
				return self.delete(request)

		elif action == 'search':
			table_values = [
				{
					"name":"form_name",
					"type":"text",
					"display":"Form name"
				},
				{
					"name":"file",
					"type":"file"
				}
			]
			list_table_values = [x["name"] for x in table_values]

			user_data = JsonConfiguration.objects.filter(Q(form_name__icontains=search)
				|Q(version__icontains=search),status_code=1).all().only(*list_table_values)

			paginator = Paginator(user_data, int(entries)) 
			page_number = request.GET.get('page')
			page_obj = paginator.get_page(page_number)
			pagination_url = request.path + "?entries=" + entries + "&search=" + search + "&action=" + action + "&"
			
			context = { 
						"data":user_data,
						"entries" : entries,
						"redirect":"json-config",
						"JsonForm":queryset_dict,
						"values":table_values,
						"page_obj" : page_obj,
	                	"pagination_url" : pagination_url,
						}          
			return render(request,'table_configuration.html',context)
		else:    
			table_values = [
				{
					"name":"form_name",
					"type":"text"
				},
				{
					"name":"file",
					"type":"file"
				}
			]
			list_table_values = [x["name"] for x in table_values]

			user_data = JsonConfiguration.objects.filter(status_code = 1).only(*list_table_values)
			paginator = Paginator(user_data, int(entries)) 
			page_number = request.GET.get('page')
			page_obj = paginator.get_page(page_number)

			if action:
				pagination_url = request.path + "?entries=" + entries + "&action=" + action + "&"          
			else:
				pagination_url = request.path + "?entries=" + entries + "&"


			starting_sr_no = (page_obj.number - 1) * int(entries) + 1

                
			context = {
					"data":user_data,
					"redirect":"json-config",
					"values":table_values,
					"JsonForm": queryset_dict,
					"entries" : entries,
					"page_obj" : page_obj,
	               	"pagination_url" : pagination_url,
	               	"starting_sr_no":starting_sr_no
				}
			return render(request,'table_configuration.html',context)

	# Create
	def post(self,request,*args, **kwargs):
		if '_put' in request.POST:
			return self.put(request)

		file = request.FILES.get('file')
		form_name = request.POST.get('form_name')
		version = request.POST.get('version')

		try:
			if file:
				f = file.read()
				file_data = json.loads(f)
				schema = {
					"type":"object"
				}
				validate(instance=file_data, schema=schema)
				user_data = JsonConfiguration.objects.create(file=file, form_name=form_name,version=version,created_at=datetime.now())

				createFiles(file_data,form_name)

				path = createZip(form_name)
				
				filename = form_name+".zip"
				
				file_wrapper = FileWrapper(open(path, 'rb'))
				file_mimetype = mimetypes.guess_type(path)
				
				response = HttpResponse(file_wrapper, content_type=file_mimetype)
				response['X-Sendfile'] = path
				response['Content-Length'] = os.stat(path).st_size
				response['Content-Disposition'] = 'attachment; filename=%s' % filename + ".zip"
				
				return response

		except Exception as ex:
			# Render create1.html with error message
			messages.error(request, (f'Please Enter your Json in Correct Format:{ex}'))
			print(ex)

			file = self.queryset
			queryset_dict = json.loads(file)
			context = {
				"JsonForm":queryset_dict,
				"redirect":"json-config",
				"starting_sr_no":starting_sr_no
			}       
			return render(request, 'create_configuration.html', context)


		user_data = JsonConfiguration.objects.create(file=file, form_name=form_name,
			version=version,created_at=datetime.now())

		if user_data:
			return redirect('json-config')

	# Edit
	def put(self,request,*args,**kwargs):

		file = request.FILES.get('file', None)
		form_name = request.POST.get('form_name', None)
		version = request.POST.get('version', None)
		created_at = request.POST.get('created_at', None)
		updated_at = request.POST.get('updated_at',None)
		id   = request.POST.get('id',None)

		if file:
			update = JsonConfiguration.objects.filter(id=id).update(file=file, 
				form_name=form_name,version=version, created_at=datetime.now())
		else:
			old_data = JsonConfiguration.objects.get(id=id)
			file = old_data.file

			update = JsonConfiguration.objects.filter(id=id).update(file=file, 
				form_name=form_name,version=version, created_at=datetime.now())

		if update:
			return redirect('json-config')
		else:
			return HttpResponse("Not updated")

	# Delete
	def delete(self,request,*args,**kwargs):

		id = request.GET.get('id',None)

		update = JsonConfiguration.objects.filter(id=id).update(status_code=0)

		if update:
			return JsonResponse({'status': 'Deleted'})
		else:
			return JsonResponse({'status': 'Not Deleted'})



