import os
from datetime import datetime 
import shutil
import json
from decouple import config
from jinja2 import Environment, FileSystemLoader
import time


'''
	function: Creates code for views and models
	input: JSON(json) and form name(string) submitted by the user
	output: Updated files according to the json in generated_application folder
'''

ZIP_FILE_PATH=config('ZIP_FILE_PATH')
GENERATED_FILES_PATH=config('GENERATED_FILES_PATH')
SCRIPTS_PATH=config('SCRIPTS_PATH')

PATH = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_ENVIRONMENT = Environment( autoescape=False, 
	loader=FileSystemLoader(os.path.join(PATH, 'templates')), trim_blocks=False)


def render_template(template_name, JSON):
    return TEMPLATE_ENVIRONMENT.get_template(template_name).render(JSON)


#Creates Files, models.py, views.py.... etc
def createFiles(JSON,form_name):
	path = os.getcwd()

	generation_time = datetime.now()
	generation_time = generation_time.strftime("%H:%M:%S %d-%m-%Y")

	# writing the form name in form-name format
	url_name = form_name.lower()
	url_name = url_name.replace(" ","-")

	# Provision for new line and 2 tabs for indentation in get function
	request_fields = "\n\t\t"
	add_update_fields = ""
	search_fields = ""
	file_save = ""
	date_variable = ""
	d_variable = ""

	html_fields = JSON['HTML_fields']
	search_list = JSON['HTML_table']['searchable_fields']


	# Generating the fetching code lines
	for field in html_fields:
		if field['type'] == 'file':
			request_fields = request_fields+f"{field['name']} = request.FILES.get('{field['name']}',None)\n\t\t"
			file_save = file_save + "obj."+f"{field['name']}= {field['name']}\n\t\t\t"

		elif field['type'] == 'checkbox':
			request_fields = request_fields+f"{field['name']} = request.POST.getlist('{field['name']}', None)\n\t\t"
		else:
			if(field['tag'] != 'button'):
				request_fields = request_fields+f"{field['name']} = request.POST.get('{field['name']}', None)\n\t\t"

	# Generating the code for creating and updating the fields in database
	for i,field in enumerate(html_fields):
		if(i==len(html_fields)-1):
			if(field['tag'] != 'button'):
				add_update_fields = add_update_fields + f"{field['name']} = {field['name']}"
		else:
			if(field['tag'] != 'button'):
				add_update_fields = add_update_fields + f"{field['name']} = {field['name']}, "
	
	# Generating code for search query
	for i,field in enumerate(search_list):		
		if(i==len(search_list)-1):
			search_fields = search_fields + f"Q({field}__icontains=search)"
		else:
			search_fields = search_fields + f"Q({field}__icontains=search)|"		


	# Updating the code written in Views.txt
	with open(os.path.join(path, SCRIPTS_PATH ,"Views.txt"), 'r') as file:			
		views = file.read()
		
		views = views.replace('$CREATEDTIME',generation_time)
		views = views.replace('$USERNAME','USER NAME ')
		views = views.replace('$CLASSNAME',f"{JSON['Model_fields']['tableName']}View")
		views = views.replace('$FORMFILTER',form_name)
		views = views.replace('$REDIRECT',url_name)
		views = views.replace('$MODELNAME',JSON['Model_fields']['tableName'])
		views = views.replace('$REQUEST_IMPORT',request_fields)
		views = views.replace('$ADD_UPDATE_FIELDS',add_update_fields)
		views = views.replace('$SEARCH_QUERY',search_fields)
		views = views.replace('$FILE_SAVE', file_save)


		# Writing the code in views.py
		with open(os.path.join(path, GENERATED_FILES_PATH ,"views.py"), 'w+') as fp:

			for i in JSON['Model_fields']['tableFields']:

				if i['type'] == 'DateField':

					d_variable = d_variable + f"date_{i['name']} = datetime.strftime(data.{i['name']}, '%Y-%m-%d')\n\t\t\t\t"
					d_variable = d_variable + f"date_{i['name']}_obj = datetime.strptime(date_{i['name']},'%Y-%m-%d')\n\n\t\t\t\t"

					date_variable = date_variable + f"'date_{i['name']}': date_{i['name']}, "
		
				elif i['type'] == 'DateTimeField':

					d_variable = d_variable + f"dtime_{i['name']} = data.{i['name']}.strftime('%Y-%m-%dT%H:%M')\n\t\t\t\t"
					d_variable = d_variable + f"dtime_{i['name']}_obj = datetime.strptime(dtime_{i['name']}, '%Y-%m-%dT%H:%M')\n\n\t\t\t\t"
					
					date_variable = date_variable + f"'dtime_{i['name']}': dtime_{i['name']},"

				elif i['type'] == 'TimeField':
					d_variable = d_variable + f"time_{i['name']} = data.{i['name']}.strftime('%H:%M')\n\t\t\t\t"
					d_variable = d_variable + f"time_{i['name']}_obj = datetime.strptime(time_{i['name']}, '%H:%M')\n\n\t\t\t\t"

					date_variable = date_variable + f"'time_{i['name']}': time_{i['name']},"

			views = views.replace('$DVARIABLE', d_variable)
			views = views.replace('$DATE_VARIABLE', date_variable)

			fp.write(views)
		

	# Writing the code in models
	# Creating the models code as per JSON
	with open(os.path.join(path, GENERATED_FILES_PATH,"models.py"), 'w+') as fp:
		fp.write("from django.db import models\n")
		fp.write("from phonenumber_field.modelfields import PhoneNumberField\n")
		fp.write("import datetime\n")

		fp.write(f"\nclass {JSON['Model_fields']['tableName']}(models.Model):\n\t")
		fp.write(f"status_code = models.BooleanField(default=1)\n\t")

		for i in JSON['Model_fields']['tableFields']:
			if i['type'] == 'CharField':
				fp.write(f"{i['name']} = models.{i['type']}(max_length={i['maxLength']}, blank={i['isBlank']}, null={i['isNull']})\n\t")
			
			elif i['type'] == 'IntegerField' or i['type'] == 'BooleanField':
				fp.write(f"{i['name']} = models.{i['type']}(default={i['default']}, blank={i['isBlank']}, null={i['isNull']})\n\t")
			
			elif i['type'] == 'PhoneNumberField':
				fp.write(f"{i['name']} = {i['type']}(blank={i['isBlank']}, null={i['isNull']})\n\t")
			
			elif i['type'] == 'EmailField':
				fp.write(f"{i['name']} = models.{i['type']}(max_length={i['maxLength']},blank={i['isBlank']}, null={i['isNull']})\n\t")
			
			elif i['type'] == 'DateField' or i['type'] == 'DateTimeField' or i['type'] == 'TimeField':
				fp.write(f"{i['name']} = models.{i['type']}(blank={i['isBlank']}, null={i['isNull']})\n\t")
			
			elif i['type'] == 'FileField':
				fp.write(f"{i['name']} = models.{i['type']}(upload_to='{i['filePath']}',blank={i['isBlank']}, null={i['isNull']})\n\t")
			
			elif i['type'] == 'ForeignKey':
				fp.write(f"{i['name']} = models.{i['type']}({i['foreignKeytablename']}, on_delete=models.CASCADE,blank={i['isBlank']}, null={i['isNull']})\n\t")	
			else:	
				pass


	# Creates create.html template
	fname = "create.html"
	with open(os.path.join(path, 'generated_application/templates' ,fname), 'w+') as f:

		create_html = render_template(fname, JSON)
		f.write("{% extends 'base.html' %}\n")
		f.write("{% load static %}\n")
		f.write("{% block content %}\n\n")
		create_html = create_html.replace("\% url redirect %/", "{% url redirect %}")
		create_html = create_html.replace("\% csrf_token %/", "{% csrf_token %}")
		f.write(create_html)
		f.write("{% endblock content %}\n\n")
		f.write("{% block script %}\n")
		f.write("""<script src="{% static 'assets/js/checkboxValidation.js' %}"></script>\n""")
		f.write("{% endblock script %}")

	# Creates edit.html template
	edit_temp = "edit.html"
	with open(os.path.join(path, 'generated_application/templates' ,edit_temp), 'w+') as f:

		edit_html = render_template(edit_temp, JSON)
		f.write("{% extends 'base.html' %}\n")
		f.write("{% load static %}\n")
		f.write("{% block content %}\n\n")
		edit_html = edit_html.replace("\% url redirect %/", "{% url redirect %}")
		edit_html = edit_html.replace("\% csrf_token %/", "{% csrf_token %}")
		edit_html = edit_html.replace("\% isCheck data '{{i.name}}' '{{value}}' as ischecked %/", "{% isCheck data '{{i.name}}' '{{value}}' as ischecked %}")
		edit_html = edit_html.replace("\%", "{%")
		edit_html = edit_html.replace("%/", "%}")
		edit_html = edit_html.replace("\% if ischecked %/ checked \% endif %/", "{% if ischecked %} checked {% endif %}")
		edit_html = edit_html.replace("\% if data.i.name == {{k}} %/ selected \% endif %/", "{% if data.i.name == {{k}} %} selected {% endif %}")
		edit_html = edit_html.replace("\% if data.i.name == '{{value}}' %/ checked \% endif %/", "{% if data.i.name == '{{value}}' %} checked {% endif %}")
		edit_html = edit_html.replace("{\{data.id}/}", "{{data.id}}")
		edit_html = edit_html.replace("\\", "{")
		edit_html = edit_html.replace("//", "}}")

		f.write(edit_html)
		f.write("{% endblock content %}\n\n")
		f.write("{% block script %}\n")
		f.write("""<script src="{% static 'assets/js/checkboxValidation.js' %}"></script>\n""")
		f.write("{% endblock script %}")
				
	# Writing the json in form.json file
	with open(os.path.join(path, 'generated_application/form_jsons', form_name + '.json'), 'w+') as fp:
		updated_json = str(JSON)
		updated_json = updated_json.replace("'","\"")
		updated_json = updated_json.replace('$FORMFILTER', form_name)
		fp.write(updated_json)

	# Writing the base template essentials in base.html file
	with open(os.path.join(path, SCRIPTS_PATH ,"base.txt"),"r") as file:
		base_html = file.read()
		with open(os.path.join(path,"generated_application/templates/base.html"),"w+") as fp:
			fp.write(base_html)


	# Writing the table essentials in table.html file
	with open(os.path.join(path, SCRIPTS_PATH ,"table.txt"),"r") as file:
		html = file.read()
		with open(os.path.join(path,"generated_application/templates/table.html"),"w+") as fp:
			fp.write(html)


	# Writing urls to the urls.py file in generated files folder
	with open(os.path.join(path, SCRIPTS_PATH, "urls.txt"), "r") as file:
		urls = file.read()
		urls = urls.replace('$REDIRECT',url_name)
		urls = urls.replace('$CLASSNAME',f"{JSON['Model_fields']['tableName']}View")

		with open(os.path.join(path, "generated_application/urls.py"), "w+") as fp:
			fp.write(urls)


	# Writing custom tags to the template_tags.py file in generated files folder
	with open(os.path.join(path,SCRIPTS_PATH,"custom_tags.txt"),"r") as file:
		tags = file.read()
		
		with open(os.path.join(path, "generated_application/templatetags/custom_tags.py"),"w+") as fp:
			fp.write("#REFER TO https://docs.djangoproject.com/en/4.1/howto/custom-template-tags/ FOR MORE UNDERSTANDING\n")
			fp.write("#MAKE SURE THE FILTER NAMES ARE NOT IN CONFLICT WITH PRE-EXISTING TAGS CREATED BY YOU")
			fp.write("\n\n\n\n")

			fp.write(tags)

	return True	


#function: Generates code for Crreating zip file 
def createZip(filename):
	path = os.getcwd()
	output_filename = filename.lower()
	output_filename = output_filename.replace(" ","-")
	zip_path = os.path.join(path, ZIP_FILE_PATH, output_filename)

	shutil.make_archive(zip_path, 'zip', "generated_application")
	time.sleep(5)
	zip_path = zip_path+".zip"

	return zip_path


