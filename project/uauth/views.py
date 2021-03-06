from django.shortcuts import render_to_response,render
from django.template import RequestContext
from project.uauth import forms
from project.apps.data.models import MyUser
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import string
import os
import random
from django.db import IntegrityError
# Create your views here.
'''def Login(request):
	if request.method=="POST":
		print("In Post")
		login_form=forms.Login_Form(request.POST)
		print(login_form.errors)
		if login_form.is_valid():
			cd=login_form.cleaned_data
			unm=cd.get('username')
			pass1=cd.get('password')
			obj=MyUser.objects.filter(username=unm).exists()
			if obj:
				uobj=MyUser.objects.get(username=unm)
				if uobj.check_password(pass1):
					request.session['user']=unm
					request.session['pass']=pass1
					return HttpResponseRedirect("/home")
				else:
					error_pass="Wrong Password"
					ctx={'login_form':login_form,'error':error_pass}
					return render_to_response('login.html',ctx,context_instance=RequestContext(request))
			else:
				error_username="Invalid Username"
				ctx={'login_form':login_form,'error':error_username}
				return render_to_response('login.html',ctx,context_instance=RequestContext(request))
		else:
			pass
	else:
		login_form=forms.Login_Form()
	ctx={'login_form':login_form}
	return render_to_response('login.html',ctx,context_instance=RequestContext(request))
'''



def Login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/home/')
	if request.method=="POST":
		login_form=forms.Login_Form(request.POST)
		if login_form.is_valid():
			cd=login_form.cleaned_data
			unm=cd.get('username')
			pass1=cd.get('password')
			user1=authenticate(username=unm,password=pass1)
			if user1 is not None:
				login(request,user1)
				u=MyUser.objects.get(email=unm)
				if not u.is_confirmed:
					return HttpResponseRedirect('/set/password')
				else:
					return HttpResponseRedirect('/home/')
			else:
				error="Invalid Username Or Password"
				ctx={'login_form':login_form,'error':error}
				return render_to_response('login.html',ctx,context_instance=RequestContext(request))
		else:
			ctx={'login_form':login_form}
			return render_to_response('login.html',ctx,context_instance=RequestContext(request))
	else:
		login_form=forms.Login_Form()
		ctx={'login_form':login_form}
		return render_to_response('login.html',ctx,context_instance=RequestContext(request))
'''
def Login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/home/')
	if request.method=="POST":
		login_form=forms.Login_Form(request.POST)
		if login_form.is_valid():
			cd=login_form.cleaned_data
			unm=cd.get('username')
			pass1=cd.get('password')
			user1=authenticate(username=unm,password=pass1)
			if user1 is not None:
				login(request,user1)
				return HttpResponseRedirect('/home/')
			else:
				ctx={'login_form':login_form}
				return render_to_response('login.html',ctx,context_instance=RequestContext(request))
		else:
			ctx={'login_form':login_form}
			return render_to_response('login.html',ctx,context_instance=RequestContext(request))
	else:
		login_form=forms.Login_Form()
		ctx={'login_form':login_form}
		return render_to_response('login.html',ctx,context_instance=RequestContext(request))
'''
def Logout(request):
	logout(request )
	return HttpResponseRedirect('/login'	)

@login_required
def ChangePassword(request):
	uobj=MyUser.objects.get(username=request.user)
	username=str(uobj.first_name)+" "+uobj.last_name
	error_message=""
	if request.method=="POST":
		change_form=forms.ChangePasswordForm(request.POST)
		if change_form.is_valid():
			cd=change_form.cleaned_data
			opass=cd.get('oldpassword')
			npass=cd.get('newpassword')
			npass_confirm=cd.get('newpassword_confirm')
			if uobj.check_password(opass):
				if npass==npass_confirm:
					uobj.set_password(npass)
					uobj.save()
					return render_to_response('change_password_succesful.html')
				else:
					error_message="New Password not Matched"
			else:
				error_message="Old Password Incorrect"
	else:
		change_form=forms.ChangePasswordForm()
	ctx={'error':error_message,'username':username,'form':change_form}
	return render_to_response('change_password.html',ctx,context_instance=RequestContext(request))
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))
def NewUserRegister(request):
	try:
		logout(request)
	except:
		pass
	if request.method=="POST":
		form=forms.NewUserRegisterForm(request.POST)
		if form.is_valid():
			cd=form.cleaned_data
			mail=cd.get('email')
			fnm=cd.get('first_name')
			lnm=cd.get('last_name')
			u=MyUser(username=mail,email=mail,first_name=fnm,last_name=lnm)
			pass1=id_generator()
			u.set_password(raw_password=pass1)
			error=""
			try:
				u.save()
				send_mail('from jp5 forum','Dear %s %s, you have successfully registered for the jp5forum.com and your confirmation password is %s.Use this password to confirm your account.A Technical Forum Site By jp5 Team Vaibhav Kumbhar & Akshay Habbu & Machchindra Pol.Thanks for Registration.'%(u.first_name,u.last_name,pass1),'tysemminiproject@gmail.com',
					[str(u.email)], fail_silently=True)
				return HttpResponseRedirect('/register_success')
			except IntegrityError:
				error="Already registered with this email.."
				ctx={'form':form,'error':error,'exists':True}
				return render_to_response("register.html",ctx,context_instance=RequestContext(request))
			
	else:
		form=forms.NewUserRegisterForm()
	ctx={'form':form}
	return render_to_response("register.html",ctx,context_instance=RequestContext(request))


@login_required
def SetPassword(request):
	if not request.user.is_authenticated():
		return redirect_to_login('/login')
	error_message=""
	if request.method=="POST":
		form=forms.SetPasswordForm(request.POST)
		if form.is_valid():
			cd=form.cleaned_data
			npass1=cd.get('new_password1')
			npass2=cd.get('new_password2')
			uobj=MyUser.objects.get(email=request.user)
			if npass1==npass2:
				uobj.set_password(npass1)
				uobj.is_confirmed=True
				uobj.save()
				return HttpResponseRedirect('/completeprofile')
			else:
				error_message="New Password not Matched"
		else:
			error="Enter Password Corresctly"
	else:
		form=forms.SetPasswordForm()
	ctx={'form':form,'error':error_message}
	return render_to_response('setpassword.html',ctx,context_instance=RequestContext(request))

def register_success(request):
	return render(request,"register_success.html")


@login_required
def ChangePassword(request):
	uobj=MyUser.objects.get(username=request.user)
	username=str(uobj.first_name)+" "+uobj.last_name
	error_message=""
	if request.method=="POST":
		change_form=forms.ChangePasswordForm(request.POST)
		if change_form.is_valid():
			cd=change_form.cleaned_data
			opass=cd.get('oldpassword')
			npass=cd.get('newpassword')
			npass_confirm=cd.get('newpassword_confirm')
			if uobj.check_password(opass):
				if npass==npass_confirm:
					uobj.set_password(npass)
					uobj.save()
					return render_to_response('change_password_succesful.html')
				else:
					error_message="New Password not Matched"
			else:
				error_message="Old Password Incorrect"
	else:
		change_form=forms.ChangePasswordForm()
	ctx={'error':error_message,'username':username,'form':change_form}
	return render_to_response('change_password.html',ctx,context_instance=RequestContext(request))
