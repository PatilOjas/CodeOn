from django.db.models import query
from django.shortcuts import redirect, render
from editor.forms import RegistrationModel
from editor.models import Register
from django.contrib.auth import authenticate, login
import compilerConnection

def homepage(request):
	if request.method == 'POST':
		if 'signup' in request.POST:
			form = RegistrationModel(request.POST)
			if form.is_valid():
				form.save()
				return redirect('editor/')
		if 'login' in request.POST:
			email = request.POST['email']
			password = request.POST['password']
			print(email, password)
			# user = authenticate(request, username=username, password=password)
			try:
				query = Register.objects.filter(email__startswith=email, password__startswith=password)[0]
				print("Query", query.email, query.password)
				return redirect('editor/')
			except:
				return redirect('/')
	return render(request, 'login.html')

def editorPage(request):
	if request.method == 'POST':
		print(request.POST['language'])
		print(request.POST['code'])
		codeprint = compilerConnection.compilerConnJava(request.POST['code'])
		print(codeprint)
	return render(request, 'index.html')