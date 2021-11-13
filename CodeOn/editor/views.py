from django.db.models import query
from django.shortcuts import redirect, render
from editor.forms import RegistrationModel
from editor.models import Register
from django.contrib.auth import authenticate, login
from compilerConnection import CompilerConn
from django.template import RequestContext
# from django.template import Context

compilerconn = CompilerConn()

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
	# context = Context({'result':False})
	global compilerconn
	context = {'result':False}
	codeprint = ""
	if request.method == 'POST':
		print(request.POST['language'])
		print(request.POST['code'])
		if request.POST['language'] == '.java':
			codeprint = compilerconn.compilerConnJava(request.POST['code'])
		elif request.POST['language'] == '.py':
			codeprint = compilerconn.compilerConnPython(request.POST['code'])
		else:
			codeprint = compilerconn.compilerConnCPP(request.POST['code'])

		print(codeprint)
		context['result'] = codeprint
	
	return render(request, 'index.html', context)
