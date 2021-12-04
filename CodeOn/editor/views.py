from time import time
from django.db.models import query
from django.shortcuts import redirect, render
from editor.forms import RegistrationModel
from editor.models import Register, Codes
from django.contrib.auth import authenticate, login
from compilerConnection import CompilerConn
from randomQuestion import QuestionProvider
from django.template import RequestContext
import xmlrpc.client
import secrets
import socket
import threading
import time
# from django.template import Context

compilerconn = CompilerConn()
curr_user = 1

def homepage(request):
	global curr_user, question, q_id
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


def timeOver(request):
	return redirect(request, 'timeup.html')

def timeup(req, clientSocket):
	if clientSocket.recv(1024).decode().strip() == "Time Up!!!!":
		return redirect('timeup')
def call(sec):
	print(sec, type(sec))
	time.sleep(2)
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientSocket.connect(("127.0.0.1", 4441))
	txt = """{'secret':'""" +  sec + """'}"""
	clientSocket.send(txt.encode())



def editorPage(request):
	global compilerconn
	global curr_user											
	context = {'result':False, 'code':""}

	question, q_id = QuestionProvider().randomPicker()
	context['question'] = question['question']
	context['time'] = question['time']
	context['secret'] = str(secrets.token_hex(16))


	try:
# Creates a socket and if it fails, it will raise an error
		clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("Socket creation successfull!!!")
	except socket.error:
		print("Socket creation failed with error", str(socket.error))

	# Default port for server 
	portNo = 4441

	# Connects to server
	try:
		clientSocket.connect(("127.0.0.1", portNo))
		print("Connection successfull!!!")
	except socket.error:
		print("Failed to connect with error", socket.error)

	clock = """{'secret':'""" +  context['secret'] + """', 'time': """ + context['time']  + """}"""

	clientSocket.send(clock.encode())
	tid = threading.Thread(target=timeup, args=(request, clientSocket,))
	tid.start()
	tid = threading.Thread(target=call, args=(context['secret'],))
	tid.start()

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
			# proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:9001/")
			# proxy.db1U(props)
			# proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:9002/")
			# proxy.db2U(props)
		else:
			#create
			codes = Codes()
			codes.userid = curr_user
			codes.qid = q_id
			codes.code = request.POST['code']
			codes.save()
			# proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:9001/")
			# proxy.db1C(props)
			# proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:9002/")
			# proxy.db2C(props)
		
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
