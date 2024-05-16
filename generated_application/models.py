from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import datetime

class Project(models.Model):
	status_code = models.BooleanField(default=1)
	name = models.CharField(max_length=100, blank=True, null=True)
	client = models.CharField(max_length=100, blank=True, null=True)
	