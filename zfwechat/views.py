# -*- coding:utf-8 -*-
import sys
import json
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
from zfwechat.models import *
from util import *
from lingnanedu import *
from django import forms
from time import clock
from django.template import loader,Context


reload(sys)
sys.setdefaultencoding('utf-8')

class UserForm(forms.Form):
	username = forms.CharField(max_length=12, min_length=6, required=True,widget=forms.TextInput(attrs={'placeholder': u'请输入你的学号...'}),)
	password = forms.CharField( min_length=6,required=True,widget=forms.PasswordInput(attrs={'placeholder': u'请输入你的密码...'},))
	isAutoLogin = forms.BooleanField(required=False)
	isRemember = forms.BooleanField(required=False)

def getMark(request):
	student = json.loads(request.session['student'], object_hook=dict2student)
	all_mark_obj = LingnanMark().getMark(student.studentNo,student.studentPsw, student.name)
	return render_to_response('mark.html',{'all_mark_obj': all_mark_obj, 'name' : student.name })

def main(request):
	student = json.loads(request.session['student'], object_hook=dict2student)
	return render_to_response('index.html', {'name', student.name})

def login(request):
	#提交表单
	if request.method == 'POST':
		start = clock()
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
			result = LingnanMark().login(student.studentNo,student.studentPsw)
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
			result = LingnanMark().login(student.studentNo,student.studentPsw)
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
			print request.COOKIES['password']
			form = UserForm(initial={'username':request.COOKIES['username'],'password':request.COOKIES['password']})
			return render_to_response('login.html',{'form':form})

	form = UserForm()
	return render_to_response('login.html',{'form':form})

def logout(request):
	form = UserForm()
	response = HttpResponseRedirect('login')
	response.delete_cookie('username')
	response.delete_cookie('password')
	del request.session['student']
	return response

def page_not_found(request):
	return HttpResponse(content="page_not_found")

def page_error(request):
	return HttpResponse(content="page_error")

def getLesson(request):
	#从session获取信息
	student = json.loads(request.session['student'], object_hook=dict2student)
	template = loader.get_template('lessons.html')
	lessons = LingnanMark().getLesson(student.studentNo, student.studentPsw, student.name)
	context = Context({'lessons':lessons, 'name':student.name})
	return HttpResponse(template.render(context))

def getGradePoint(request):
	student = json.loads(request.session['student'], object_hook=dict2student)
	avgGradePoint = LingnanMark().getAvgGradePoint(student.studentNo, student.studentPsw)
	return render_to_response('gradepoint.html', {'avgGradePoint': avgGradePoint, 'name': student.name })

def doGet(request):
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
		#if dict.has_key('Event'):
		#	dict['MsgType'] = 'text'
		#	dict['Content'] = u'<a href="http://dweimaql.tunnel.qydev.com/wechat/login" >欢迎关注！点此登录 </a>'
		#dict['MsgType'] = 'news'
		#dict['Title'] = 'hehe'
		#dict['Description'] = 'laile'
		#dict['PicUrl'] = ''
		#dict['Url'] =  'http://mp.weixin.qq.com/s?__biz=MzAwOTgwODc5MQ==&tempkey=dMkY26v8Rd75CPTkFQovft0mbl6NIU57x6xopcM0icpVVsjNQEjYoJSRuHtUNiLrdrrdO2vPm8Ls2sYRSOfHLBPMsOkjrsUaTgJTYLR73tLLPbV5UfvSmr3XZWBY4q75fw4WiidkER0Hhbx0%2BVsibw%3D%3D&#rd'#'http://dweimaql.tunnel.qydev.com/wechat/login'
		return HttpResponse(xml_result)		

	return HttpResponse('none')

