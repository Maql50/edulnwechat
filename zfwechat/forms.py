# encoding:utf-8
import sys
from django import forms

reload(sys)
sys.setdefaultencoding('utf-8')

class UserForm(forms.Form):
	'''用户登录表单'''
	username = forms.CharField(max_length=12, min_length=6, required=True,widget=forms.TextInput(attrs={'placeholder': u'请输入你的学号...'}),)
	password = forms.CharField( min_length=6,required=True,widget=forms.PasswordInput(attrs={'placeholder': u'请输入你的密码...'},))
	isAutoLogin = forms.BooleanField(required=False)
	isRemember = forms.BooleanField(required=False)

class EmailForm(forms.Form):
	'''用户邮箱'''
	email = forms.CharField(max_length=55, required=True)