from django import forms
from django.db.models import fields
from .models import Register

class RegistrationModel(forms.ModelForm):
	class Meta:
		model = Register
		fields = ('name', 'email', 'password')
