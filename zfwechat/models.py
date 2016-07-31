from django.db import models

class Student(object):
	def __init__(self, studentNo, studentPsw, name):
		self.studentNo = studentNo
		self.studentPsw = studentPsw
		self.name = name

def student2dict(student):
	return {'studentNo':student.studentNo,'studentPsw':student.studentPsw,'name':student.name}

def dict2student(dict):
	return Student(dict['studentNo'], dict['studentPsw'], dict['name'])

class AccessToken(object):
	@property
	def token(self):
	    return self._token
	
	@token.setter
	def token(self, token):
	    self._token = token

	@property
	def expiresIn (self):
		return self._expiresIn

	@expiresIn.setter
	def expiresIn (self, expiresIn):
		self._expiresIn = expiresIn

class StudentModel(models.Model):
 	studentNo = models.CharField(max_length=11)
 	studentPsw = models.CharField(max_length=255)
 	email = models.CharField(max_length=55)
 	markNum = models.IntegerField(max_length=11)

 	def __unicode__(self):
 		return self.studentNo+" "+ self.studentPsw+" "