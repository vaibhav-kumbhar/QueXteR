from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from project.apps.homepage import forms
from project.uauth import forms as auth_forms
from project.apps.data.models import User_Profile,MyUser
from django.template import RequestContext
from django.core.mail import send_mail
from django.core import mail
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from socket import gaierror
from random import choice
import string
import random
# Create your views here.
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


def register_form(request):
	if request.method=="POST":
		reg_form=forms.register_form(request.POST)
		if reg_form.is_valid():
			cd=reg_form.cleaned_data
			fname=cd.get('fname')
			lname=cd.get('lname')
			email1=cd.get('email')
			gen=cd.get('gender')
			dob=cd.get('dob')
			profession=cd.get('profession')
			institute=cd.get('institute')
			qualification=cd.get('qualification')
			city=cd.get('city')
			state=cd.get('state')
			country=cd.get('country')

			u=MyUser()
			u.username=email1
			u.email=email1
			u.first_name=fname
			u.last_name=lname
			pass1=id_generator()
			u.set_password(raw_password=pass1)
			print(pass1)
			up=User_Profile(gender=gen)
			up.dob=dob
			up.profession=profession
			up.institute_name=institute
			up.qualification=qualification
			up.city=city
			up.state=state
			up.country=country
			

			u.save()
			up.mid=u
			up.save()
			send_mail('from jp5 forum','Dear %s %s, you have successfully registered for the jp5forum.com and your password is %s.A Technical Forum Site By jp5 Team Vaibhav Kumbhar & Akshay Habbu & Machchindra Pol.Thanks for Registration.'%(u.first_name,u.last_name,pass1),'tysemminiproject@gmail.com',
				[str(u.email)], fail_silently=True)
			HttpResponseRedirect("login.html")
	else:
		reg_form=forms.register_form()
	ctx1={'reg_form':reg_form}
	return render_to_response("register.html",ctx1,context_instance=RequestContext(request))


@login_required
def edit_pro_form(request):
	nonU=MyUser.objects.get(email=request.user)
	try:
		nonUP=User_Profile.objects.get(mid=request.user)
	except ObjectDoesNotExist:
		u=User_Profile(mid=nonU)
		u.save()
		nonUP=User_Profile.objects.get(mid=request.user)
	if request.method=="POST":
		editeduser=auth_forms.edituser_form(request.POST,instance=nonU)
		editedprofile=auth_forms.editprofile_form(request.POST,instance=nonUP)
		if editeduser.is_valid() and editedprofile.is_valid():
			editeduser.save()
			editedprofile.save()
			return HttpResponseRedirect("/profile")
	else:
		editeduser=auth_forms.edituser_form(instance=nonU)
		editedprofile=auth_forms.editprofile_form(instance=nonUP)
	ctx1={'editeduser':editeduser,'editedprofile':editedprofile}
	return render_to_response("editprofile.html",ctx1,context_instance=RequestContext(request))

@login_required
def profile_edit_succesful(request):
	ctx={}
	return render_to_response("Profile_edit_succesful.html",ctx,context_instance=RequestContext(request))
