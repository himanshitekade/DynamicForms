from django.db import models
import jsonfield
import datetime


# Create your models here.
class JsonConfiguration(models.Model):
	file = models.FileField(upload_to="JSON_configurations")
	form_name = models.CharField(max_length=100)
	version = models.CharField(max_length=10)
	created_at = models.DateTimeField()
	updated_at = models.DateTimeField(null=True, blank=True)
	status_code = models.BooleanField(default=1)

	def __str__(self):
		return self.form_name