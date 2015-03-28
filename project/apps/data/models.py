from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class MyUser(User):
	is_confirmed=models.BooleanField(default=False);
	def __str__(self):
		return "%s"%(self.email)


class User_Profile(models.Model):
	mid=models.OneToOneField('MyUser',primary_key=True)
	gender=models.CharField(null=True,max_length=20)
	dob=models.DateField(null=True,auto_now=False,auto_now_add=False)
	profession=models.CharField(null=True,max_length=10)
	institute_name=models.CharField(null=True,max_length=200)
	qualification=models.CharField(null=True,max_length=50)
	city=models.CharField(null=True,max_length=50)
	state=models.CharField(null=True,max_length=50)
	country=models.CharField(null=True,max_length=50)


	def __str__(self):
		return "%s"%(self.mid)

class Question(models.Model):
	queid=models.AutoField(primary_key=True)
	email=models.ForeignKey('MyUser')
	que=models.TextField()
	sector=models.ManyToManyField('Sector')
	date_created=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "%s"%(self.que)

class Sector(models.Model):
	sectornm=models.CharField(primary_key=True,max_length=100)

	def __str__(self):
		return u'%s'%(self.sectornm)

class Answer(models.Model):
	ansid=models.AutoField(primary_key=True)
	email=models.ForeignKey('MyUser')
	queid=models.ForeignKey('Question')
	answer=models.TextField()
	date_answered=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "%s"%(self.answer)

class Notification(models.Model):
	user_ref=models.ForeignKey('MyUser')
	ans_ref=models.ForeignKey('Answer')
	datetime=models.DateTimeField(auto_now_add=True)
	def __str__(self):
		obj=MyUser.objects.get(email=self.ans_ref.email)
		username=str(obj.first_name)+" "+obj.last_name
		return "%s answered your question"%(username)