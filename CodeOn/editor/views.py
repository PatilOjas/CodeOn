from django.db.models import query
from django.shortcuts import redirect, render
from editor.forms import RegistrationModel
from editor.models import Register, Codes
from django.contrib.auth import authenticate, login
from compilerConnection import CompilerConn
from django.template import RequestContext
import xmlrpc.client
# from django.template import Context

compilerconn = CompilerConn()
curr_user = 1

def homepage(request):
	global curr_user
	if request.method == 'POST':
		if 'signup' in request.POST:
			form = RegistrationModel(request.POST)
			if form.is_valid():
				form.save()
				try:
					q = Register.objects.filter(email__startswith=request.POST['email'], name__startswith=request.POST['name'])[0]
					curr_user = q.id
				except:
					pass
				return redirect('editor/')
		if 'login' in request.POST:
			email = request.POST['email']
			password = request.POST['password']
			print(email, password)
			try:
				q = Register.objects.filter(email__startswith=request.POST['email'], name__startswith=request.POST['password'])[0]
				curr_user = q.id
			except:
				pass
			
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
	global curr_user
	q_id = 0 											# to be changed
	context = {'result':False, 'code':""}
	codeprint = ""
	if request.method == 'POST':
		print(request.POST['language'])
		print(request.POST['code'])
		props = {
		'userid':curr_user,
		'qid': q_id,
		'code': request.POST['code'],
		'output': codeprint
		}
		q = Codes.objects.filter(userid=curr_user, qid=q_id)
		if len(q) > 0:
			# update
			codes = q[0]
			codes.code = request.POST['code']
			codes.save()
			proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:9001/")
			proxy.db1U(props)
			proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:9002/")
			proxy.db2U(props)
		else:
			#create
			codes = Codes()
			codes.userid = curr_user
			codes.qid = q_id
			codes.code = request.POST['code']
			codes.save()
			proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:9001/")
			proxy.db1C(props)
			proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:9002/")
			proxy.db2C(props)
		if request.POST['language'] == '.java':
			codeprint = compilerconn.compilerConnJava(request.POST['code'])
		elif request.POST['language'] == '.py':
			codeprint = compilerconn.compilerConnPython(request.POST['code'])
		else:
			codeprint = compilerconn.compilerConnCPP(request.POST['code'])

		print(codeprint)
		props['output'] = codeprint
		proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:9001/")
		proxy.db1U(props)
		proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:9002/")
		proxy.db2U(props)
		q = Codes.objects.filter(userid=curr_user, qid=q_id)
		q[0].output=codeprint
		q[0].save()

		context['result'] = codeprint
		context['code'] = request.POST['code']
	
	return render(request, 'index.html', context)
