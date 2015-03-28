from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
admin.autodiscover()
from project.uauth import forms
urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	#(r'^',include('project.apps.data.urls')),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^$', 'project.apps.data.views.home',name='Home'),
	url(r'^home/$', 'project.apps.data.views.home',name='Home'),
	url(r'^register/$','project.uauth.views.NewUserRegister',name='register Form'),
	url(r'^register_success/$','project.uauth.views.register_success',name='register Success'),
	url(r'^login/$','project.uauth.views.Login',name='Login'),
	url(r'^askque/','project.apps.data.views.ask_que',name='AskQuestion'),
	url(r'^answer/','project.apps.data.views.answer_it',name='AnswerIt'),
	url(r'^logout/','project.uauth.views.Logout',name='Logout'),
	url(r'^yourque/','project.apps.data.views.yourque',name='Your Questions'),
	url(r'^question/','project.apps.data.views.question',name='Questions'),
	url(r'^profile/','project.apps.data.views.profile_view',name='My Profile'),
	url(r'^editprofile/','project.apps.homepage.views.edit_pro_form',name='Edit Profile'),
	url(r'^notifications/','project.apps.data.views.notification',name='Notifications'),
	url(r'^Profile_edit_succesful/','project.apps.homepage.views.profile_edit_succesful',name='Profile edited succesfully'),
	url(r'^Question_uploaded/','project.apps.data.views.question_uploaded',name='Profile edited succesfully'),
	url(r'^Add_sector/','project.apps.data.views.add_sector',name='Add Sector'),
	url(r'^sectorwise/','project.apps.data.views.sec_wise_disp',name='Sectorwise Display'),
	url(r'^about/','project.apps.data.views.about',name='About Us'),
	url(r'^set/password/','project.uauth.views.SetPassword',name='SetPassword'),
	url(r'^completeprofile/','project.apps.homepage.views.edit_pro_form',name='Complete Profile'),
)



urlpatterns += patterns('',

      #override the default urls
      url(r'^password/change/$',
                    auth_views.password_change,{'template_name': 'password_change.html','password_change_form':forms.PasswordChangeForm},
                    name='password_change'),
      url(r'^password/change/done/$',
                    auth_views.password_change_done,{'template_name': 'password_change_done.html'},
                    name='password_change_done'),
      url(r'^password/reset/$',auth_views.password_reset,{'template_name': 'password_reset.html','password_reset_form': forms.PasswordResetForm},name='password_reset'),
      url(r'^password/reset/done/$',
                    auth_views.password_reset_done,{'template_name': 'password_reset_done.html'},
                    name='password_reset_done'),
      url(r'^password/reset/complete/$',
                    auth_views.password_reset_complete,
                    name='password_reset_complete'),
      url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                    auth_views.password_reset_confirm,{'template_name': 'password_reset.html','set_password_form': forms.SetPasswordForm},
                    name='password_reset_confirm'),

	  
)