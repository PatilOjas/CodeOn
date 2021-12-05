from django.db import models
from django.db.models.deletion import CASCADE

class Register(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100, null=False, blank=False)
	email = models.EmailField(null=False, blank=False)
	password = models.CharField(max_length=32, null=False, blank=False)


	def __str__(self):
		return self.name

class Codes(models.Model):
	userid = models.IntegerField()
	qid = models.IntegerField()
	code = models.CharField(max_length=10000, null=False, blank=False)
	output = models.CharField(max_length=10000)
