'''
Date of creation: 18:44:08 18-03-2024
Created by: USER NAME 
'''

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .models import *
from datetime import datetime
from django.contrib import messages
import json
from django.db.models import Q
import os
from django.core.paginator import Paginator



class ProjectView(View):

	def __init__(self,*args,**kwargs):
		path = os.getcwd()

		with open(os.path.join(path, "form_jsons/Project.json"), 'r') as file:
			self.queryset = file.read()

	def get(self,request,*args, **kwargs):
		file = self.queryset 
		queryset_dict = json.loads(file)

		action = request.GET.get('action',None)
		instance_id = request.GET.get('id',None)
		search = request.GET.get('search',None)
		entries = request.GET.get('entries', '5')

		table_values = queryset_dict['HTML_table']['values']
		list_table_values = [x["name"] for x in table_values]
		
		if action == 'create':	
			context = {
				"redirect":"project"
			}       
			return render(request, 'create.html', context)

		elif action == 'edit':
			if instance_id:
				data = Project.objects.filter(status=1).get(id=instance_id)

				

				json_string = str(queryset_dict)
				context = {"data":data, "redirect":"project", }
				return render(request,'edit.html',context)

		elif action == 'delete':	
			if instance_id:
				return self.delete(request)

		elif action == 'search':
			data = Project.objects.filter(Q(name__icontains=search)|Q(client__icontains=search),status=1).all()

			paginator = Paginator(data, int(entries)) 
			page_number = request.GET.get('page')
			page_obj = paginator.get_page(page_number)
			pagination_url = request.path + "?entries=" + entries + "&search=" + search + "&action=" + action + "&"

			#TODO: Uncomment if checkbox field is included in the form.
			#for i in data:
				#var =i.checkbox.replace("[","")
				#var = var.replace("]","")
				#var = var.replace("'", "")
				#var = var.split(",")
				#i.checkbox = var
				#i.save()

			context = {
				"data":data, 
				"values":table_values, 
				"JsonForm": queryset_dict, 
				"redirect":"project",
				"entries" : entries,
				"page_obj" : page_obj,
                "pagination_url" : pagination_url,
				}
			return render(request,'table.html',context)

		else:    						
			data = Project.objects.filter(status = 1).only(*list_table_values)


			paginator = Paginator(data, int(entries)) 
			page_number = request.GET.get('page')
			page_obj = paginator.get_page(page_number)

			if action:
				pagination_url = request.path + "?entries=" + entries + "&action=" + action + "&"          
			else:
				pagination_url = request.path + "?entries=" + entries + "&"


			#TODO: Uncomment if checkbox field is included in the form.
			
			#for i in data:
				#var =i.checkbox.replace("[","")
				#var = var.replace("]","")
				#var = var.replace("'", "")
				#var = var.split(",")
				#i.checkbox = var
				#i.save()

			context = {
				"data":data,
				"redirect":"project",
				"values":table_values,
				"JsonForm": queryset_dict,
				"entries" : entries,
				"page_obj" : page_obj,
               	"pagination_url" : pagination_url
			}
			return render(request,'table.html',context)

    # Create
	def post(self,request,*args, **kwargs):
		if '_put' in request.POST:
			return self.put(request)
			
		
		name = request.POST.get('name', None)
		client = request.POST.get('client', None)
		
		
		data = Project.objects.create(name = name, client = client, )

		if data:
			return redirect('project')

    # Edit
	def put(self,request,*args,**kwargs):
		
		name = request.POST.get('name', None)
		client = request.POST.get('client', None)
		
		id   = request.POST.get('id',None)

		#TODO: Implement IF validation if file field available in the form

		#if file:
			#obj = Project.objects.get(id=id)
			#''''''
			#obj.save()
			
		# TODO: Remove file field
		update = Project.objects.filter(id=id).update(name = name, client = client, )
		
		#else: 
		#	old_data = Project.objects.get(id=id)

		#	update = Project.objects.filter(id=id).update(name = name, client = client, )

		if update:
			return redirect('project')
		else:
			return HttpResponse("Not updated")

    # Delete
	def delete(self,request,*args,**kwargs):
		id = request.GET.get('id',None)

		update = Project.objects.filter(id=id).update(status=0)
		if update:
			return redirect('project')
		else:
			return HttpResponse("Not updated")


