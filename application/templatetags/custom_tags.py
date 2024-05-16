from django import template
from django.template import Context

register = template.Library()

@register.simple_tag(name = 'isCheck')
def custom_for_check(value,arg1,arg2):	
	if arg2 in getattr(value,arg1):
		return True
	else:
		return False

@register.simple_tag(name = 'isRadio')
def custom_for_radio(value,arg1,arg2):
	if arg2 in getattr(value,arg1):
		return True
	else:
		return False

@register.filter(name="get")
def getValues(dict,key, default=''):
	value = getattr(dict,key["name"])
	
	if key["type"] == "file":
		return value.url
	elif key["name"] == "checkbox":
		print(value)
	return value
