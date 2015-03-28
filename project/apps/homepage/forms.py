from django import forms
from project.apps.data import models
from django.forms.extras.widgets import SelectDateWidget
import datetime
from project.apps.data.models import Sector


class register_form(forms.Form):
	gender_choices=(('Male','MALE'),('Female','FEMALE'))
	ylist=[]
	d=datetime.date.today()
	y=1980
	while y!=d.year-9:
		ylist.append(y)
		y+=1
	Pro_Choices=(('S','Student'),('T','Teacher'),('C','Company Employer'),('O','Other'),)

	fname=forms.CharField()
	lname=forms.CharField()
	email=forms.EmailField()
	gender=forms.ChoiceField(widget=forms.RadioSelect,choices=gender_choices)
	dob=forms.DateField(widget=SelectDateWidget(years=ylist))
	profession=forms.CharField()#widget=RadioSelect,choices=Pro_Choices))
	institute=forms.CharField()
	qualification=forms.CharField()
	city=forms.CharField()
	state=forms.CharField()
	country=forms.CharField()
	
	def clean_fname(self):
		cd=self.cleaned_data
		fname=cd.get('fname')
		if len(fname)<3:
			raise forms.ValidationError("Small Name")
		return fname
	def clean_dob(self):
		cd=self.cleaned_data
		dob=cd.get('dob')
		if dob>=datetime.date.today():
			raise forms.ValidationError("Wrong Date of Birth")
		return dob
	def clean(self):
		cd=self.cleaned_data
		return cd


class QuestionForm(forms.Form):
	l=[]
	obj=Sector.objects.all()
	for i in obj:
		a=[i,i]
		l.append(a)
	question=forms.CharField(widget=forms.Textarea)
	#sector=forms.TypedMultipleChoiceField(choices=l,required=True,empty_value='general')
	sector=forms.ModelMultipleChoiceField(queryset=Sector.objects.all(),widget=forms.CheckboxSelectMultiple,required=True)

class add_sector_Form(forms.Form):
	sector=forms.CharField()

class AnswerForm(forms.Form):
	ans=forms.CharField(widget=forms.Textarea)


'''class editpro_form(forms.Form,req):
usernm=""
	def send_user(self,a):
		usernm=a
		print(usernm)
	gender_choices=(('Male','MALE'),('Female','FEMALE'))
	ylist=[]
	d=datetime.date.today()
	y=1980
	while y!=d.year-9:
		ylist.append(y)
		y+=1
	Pro_Choices=(('S','Student'),('T','Teacher'),('C','Company Employer'),('O','Other'),)
	print(usernm)
	u=models.MyUser.objects.get(email=req.user)
	up=models.User_Profile.objects.get(username=req.user)
	fname=forms.CharField(widget=forms.TextInput(attrs={'value':u.first_name}))
	lname=forms.CharField()
	gender=forms.ChoiceField(widget=forms.RadioSelect,choices=gender_choices)
	dob=forms.DateField(widget=SelectDateWidget(years=ylist))
	profession=forms.CharField()#widget=RadioSelect,choices=Pro_Choices))
	institute=forms.CharField()
	qualification=forms.CharField()
	city=forms.CharField()
	state=forms.CharField()
	country=forms.CharField()'''




class edituser_form(forms.ModelForm):
	class Meta:
		model=models.MyUser
		fields=['first_name','last_name']

class editprofile_form(forms.ModelForm):
	class Meta:
		model=models.User_Profile
		fields=['gender','dob','profession','institute_name','qualification','city','state','country']	
		widgets={'dob':SelectDateWidget(years=range(1980,datetime.date.today().year-10)),'gender':forms.RadioSelect(choices=(('Male','MALE'),('Female','FEMALE')))}