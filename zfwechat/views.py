# coding:utf-8
import sys
#设置默认字符编码为UTF-8
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from forms import *
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
from zfwechat.models import *
from util import *
from lingnanedu import *
from time import clock
from django.template import loader,Context
from django.core import mail

def getMark(request):
	'''获取成绩请求'''
	student = json.loads(request.session['student'], object_hook=dict2student)
	all_mark_obj = ZhengFangEduSytem().getMark(student.studentNo,student.studentPsw, student.name)
	return render_to_response('mark.html',{'all_mark_obj': all_mark_obj, 'name' : student.name })

def getMain(request):
	'''获取主页面'''
	student = json.loads(request.session['student'], object_hook=dict2student)
	return render_to_response('index.html', {'name', student.name})

def login(request):
	'''用户登录'''
	#用户提交表单
	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			student = Student(data['username'], data['password'],"")
			isAutoLogin = data['isAutoLogin']
			isRemember = data['isRemember']

			#账号和密码为空
			if student.studentNo == "" or student.studentPsw == "":
				form = UserForm()
				form.failed = True
				return render_to_response('login.html',{'form':form})

			#成功则返回名称，否则返回false
			result = ZhengFangEduSytem().login(student.studentNo,student.studentPsw)
			if result == False:
				form = UserForm()
				form.failed = True
				return render_to_response('login.html',{'form':form})				

			response = render_to_response('index.html', {'name': result})
			student.name = result

			#存入session
			request.session['student'] = json.dumps(student, default=student2dict)

			#自动登录
			if isAutoLogin == True:
				response.set_cookie('isAutoLogin',True)

			if isRemember == True:
				response.set_cookie('isRemember',True)

			if isAutoLogin or isRemember:
				response.set_cookie('username',student.studentNo)
				response.set_cookie('password',student.studentPsw)

			return response

	#非表单提交	
	if "isAutoLogin" in request.COOKIES:	
		if "username" in request.COOKIES and 'password' in request.COOKIES:
			student = Student(request.COOKIES['username'],request.COOKIES['password'],"")
			#成功则返回名称，否则返回false
			result = ZhengFangEduSytem().login(student.studentNo,student.studentPsw)
			if result == False:
				form = UserForm()
				form.failed = True
				return render_to_response('login.html',{'form':form})				

			response = render_to_response('index.html', {'name': result})
			student.name = result
			#存入session
			request.session['student'] = json.dumps(student, default=student2dict)
	 		return response
 	if "isRemember" in request.COOKIES:
		if "username" in request.COOKIES and 'password' in request.COOKIES:
			form = UserForm(initial={'username':request.COOKIES['username'],'password':request.COOKIES['password']})
			return render_to_response('login.html',{'form':form})

	form = UserForm()
	return render_to_response('login.html',{'form':form})

def logout(request):
	'''退出登录'''
	form = UserForm()
	response = HttpResponseRedirect('login')
	response.delete_cookie('username')
	response.delete_cookie('password')
	#清空session
	del request.session['student']
	return response

def pageNoFound(request):
	'''404发送邮件给管理员'''
	mail.mail_admins("subject", "message", connection=None, html_message=None)
	return render_to_response('404.html')

def pageError(request):
	'''500发送邮件给管理员'''
	mail.mail_admins("subject", "message", connection=None, html_message=None)
	return render_to_response('500.html')

def getLesson(request):
	'''获取课程'''
	#从session获取信息
	student = json.loads(request.session['student'], object_hook=dict2student)
	template = loader.get_template('lessons.html')
	lessons = ZhengFangEduSytem().getLesson(student.studentNo, student.studentPsw, student.name)
	context = Context({'lessons':lessons, 'name':student.name})
	return HttpResponse(template.render(context))

def getGradePoint(request):
	'''获取平均绩点'''
	student = json.loads(request.session['student'], object_hook=dict2student)
	avgGradePoint = ZhengFangEduSytem().getAvgGradePoint(student.studentNo, student.studentPsw, student.name)
	return render_to_response('gradepoint.html', {'avgGradePoint': avgGradePoint, 'name': student.name })

def doWechat(request):
	'''接收微信服务器发送的请求'''
	if request.method == 'GET':
		signature = request.GET['signature']
		timestamp = request.GET['timestamp']
		nonce = request.GET['nonce']
		echostr = request.GET['echostr']
		if CheckUtil().checkSignature(signature, timestamp, nonce):
			return HttpResponse(echostr)
		
	if request.method == 'POST':
		xml = request.body
		util = MessageUtil()
		xml_result = util.type_handler(xml)
		return HttpResponse(xml_result)		
	return HttpResponse('none')

