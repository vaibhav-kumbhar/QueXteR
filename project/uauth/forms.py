from django import forms

from project.apps.data import models
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from django.contrib.sites.models import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template import loader
import datetime

class Login_Form(forms.Form):
	username=forms.EmailField(widget=forms.TextInput(attrs={'placeholder':"Username or email"}))	
	password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Password"}))

	def clean_password(self):
		cd=self.cleaned_data
		password=cd.get('password')
		if len(password)<1:
			raise forms.ValidationError("Please Enter Password")
		return password



class PasswordChangeForm(forms.Form):
	'''
    A form that lets a user change set his/her password without entering the
    old password'''
	error_messages = {'password_mismatch':"The two password fields didn't match.",'password_incorrect': "Your old password was entered incorrectly.Please enter it again."}
	old_password = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder':"Old Password"}))
	new_password1 = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder':"New Password"}))
	new_password2 = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder':"Confirm New Password"}))
	
	def __init__(self, user, *args, **kwargs):
		self.user = user
		super(forms.Form, self).__init__(*args, **kwargs)

	def clean_new_password2(self):
		password1 = self.cleaned_data.get('new_password1')
		password2 = self.cleaned_data.get('new_password2')
		if password1 and password2:
			if password1 != password2:
				raise forms.ValidationError(
					self.error_messages['password_mismatch'],
					code='password_mismatch',
                )
		return password2

	def clean_old_password(self):
		"""
		Validates that the old_password field is correct.
		"""
		old_password = self.cleaned_data["old_password"]
		if not self.user.check_password(old_password):
			raise forms.ValidationError(
				self.error_messages['password_incorrect'],
				code='password_incorrect',
				)
		return old_password
	def save(self, commit=True):
		self.user.set_password(self.cleaned_data['new_password1'])
		if commit:
			self.user.save()
		return self.user


class PasswordResetForm(forms.Form):
	email = forms.EmailField(max_length=254,widget=forms.TextInput(attrs={'placeholder':"Email"}))
	def save(self, domain_override=None,subject_template_name='registration/password_reset_subject.txt',email_template_name='registration/password_reset_email.html',use_https=False,token_generator=default_token_generator,from_email=None,request=None):
		'''Generates a one-use only link for resetting password and sends to the user.'''
		UserModel = get_user_model()
		email = self.cleaned_data["email"]
		active_users = UserModel._default_manager.filter(
			email__iexact=email, is_active=True)
		for user in active_users:
			# Make sure that no email is sent to a user that actually has
			# a password marked as unusable
			if not user.has_usable_password():
				continue
			if not domain_override:
				current_site = get_current_site(request)
				site_name = current_site.name
				domain = current_site.domain
			else:
				site_name = domain = domain_override
			c = {'email': user.email,
					'domain': domain,
					'site_name': site_name,
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'user': user,
					'token': token_generator.make_token(user),
					'protocol': 'https' if use_https else 'http',
				}
			subject = loader.render_to_string(subject_template_name, c)
			# Email subject *must not* contain newlines
			subject = ''.join(subject.splitlines())
			email = loader.render_to_string(email_template_name, c)
			send_mail(subject, email, from_email, [user.email])

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set his/her password without entering the
    old password
    """
    error_messages = {
		'password_mismatch':"The two password fields didn't match."
    }
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"New Password"}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"New password confirmation"}))

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    '''def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user
'''



class edituser_form(forms.ModelForm):
	class Meta:
		model=models.MyUser
		fields=['first_name','last_name']

class editprofile_form(forms.ModelForm):
	class Meta:
		model=models.User_Profile
		fields=['gender','dob','profession','institute_name','qualification','city','state','country']	
		widgets={'dob':SelectDateWidget(years=range(1980,datetime.date.today().year-10)),'gender':forms.RadioSelect(choices=(('Male','MALE'),('Female','FEMALE')))}
		labels={'dob':"Date of Birth"}

class NewUserRegisterForm(forms.Form):
	email=forms.EmailField(widget=forms.TextInput(attrs={'placeholder':"Email"}))
	first_name=forms.CharField(widget=forms.TextInput(attrs={'placeholder':"First Name"}))
	last_name=forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Last Name"}))
