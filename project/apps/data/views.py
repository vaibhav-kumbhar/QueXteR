from django.shortcuts import render_to_response
from project.apps.data import models
from django.template import RequestContext
from django.core.paginator import Paginator,InvalidPage,EmptyPage
from project.apps.homepage.forms import QuestionForm
from project.apps.homepage.forms import AnswerForm
from project.apps.homepage.forms import add_sector_Form
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# Create your views here.
@login_required
def home(request):
	#notifyme() method for giving notifications
	obj=models.Question.objects.all().order_by('-date_created')
	sec_obj=models.Sector.objects.all()
	page=request.GET.get('page')
	p=Paginator(obj,'5')
	try:
		page=int(request.GET.get('page','1'))
	except ValueError:
		page=1
	try:
		pobj=p.page(page)
	except InvalidPage:
		pobj=p.page(p.num_pages)
	qalist=[]
	for q in pobj:
		try:
			aobj=models.Answer.objects.filter(queid=q.queid).order_by('-date_answered').__getitem__(0)
		except IndexError:
			aobj=""
		user_name=models.MyUser.objects.get(username=q.email)
		try:
			answerer_name=models.MyUser.objects.get(username=aobj.email)
		except:
			answerer_name=""
		try:
			ansnm=str(answerer_name.first_name)+" "+answerer_name.last_name
		except:
			ansnm=""
		sector=q.sector.all()
		a=[q,aobj,sector,(str(user_name.first_name)+" "+user_name.last_name),ansnm]
		qalist.append(a)
	ctx={'obj':qalist,'page':pobj,'sec_obj':sec_obj}
	return render_to_response('home.html',ctx,context_instance=RequestContext(request))

@login_required
def yourque(request):
	obj=models.Question.objects.filter(email=request.user).order_by('-date_created')
	sec_obj=models.Sector.objects.all()
	page=request.GET.get('page')
	p=Paginator(obj,'5')
	try:
		page=int(request.GET.get('page','1'))
	except ValueError:
		page=1
	try:
		pobj=p.page(page)
	except InvalidPage:
		pobj=p.page(p.num_pages)
	qalist=[]
	for q in pobj:
		try:
			aobj=models.Answer.objects.filter(queid=q.queid).order_by('-date_answered').__getitem__(0)
		except IndexError:
			aobj=""
		sector=q.sector.all()
		try:
			answerer_name=models.MyUser.objects.get(username=aobj.email)
			an=str(answerer_name.first_name)+" "+answerer_name.last_name
		except:
			an=""
		a=[q,aobj,sector,an]
		qalist.append(a)
	ctx={'obj':qalist,'page':pobj,'sec_obj':sec_obj}
	return render_to_response('yourque.html',ctx,context_instance=RequestContext(request))



@login_required
def ask_que(request):
	user_obj=models.MyUser.objects.get(email__exact=request.user)
	fnm=user_obj.first_name
	lnm=user_obj.last_name
	username=str(fnm)+" "+lnm
	if request.method=="POST": 
		form=QuestionForm(request.POST)
		if form.is_valid():
			cd=form.cleaned_data
			question=cd.get('question')
		#When Session will start update the value of user email to the email field
			obj=models.Question(que=question)
			obj.email=user_obj
			obj.save()
			sect=cd.get('sector')
			obj.sector=sect
			obj.save()
			return HttpResponseRedirect('/yourque')
	else:
		form=QuestionForm()
	ctx={'form':form,'users':username}
	return render_to_response("askque.html",ctx,context_instance=RequestContext(request))

@login_required
def add_sector(request):
	sec_obj=models.Sector.objects.all()
	if request.method=="POST":
		form=add_sector_Form(request.POST)
		if form.is_valid():
			cd=form.cleaned_data
			sect=cd.get('sector')
			sec=models.Sector()
			sec.sectornm=sect
			sec.save()
	else:
		form=add_sector_Form()
	sec_obj.order_by('sectornm')
	ctx={'form':form,'sec_obj':sec_obj}
	return render_to_response("Add_sector.html",ctx,context_instance=RequestContext(request))


@login_required
def answer_it(request):
	id1=request.GET.get('question')
	que=models.Question.objects.get(queid=id1)
	que_user_obj=models.MyUser.objects.get(email=que.email)
	if request.method=="POST":
		form=AnswerForm(request.POST)
		if form.is_valid():
			cd=form.cleaned_data
			ans=cd.get('ans')
			obj=models.Answer()
			obj.answer=ans
			ans_user_obj=models.MyUser.objects.get(email=request.user)
			obj.email=ans_user_obj
			obj.queid=que
			obj.save()
			if que_user_obj == ans_user_obj:
				pass
			else:
				nobj=models.Notification()
				nobj.user_ref=que_user_obj
				nobj.ans_ref=obj
				nobj.save()
			return HttpResponseRedirect('/')
	else:
		form=AnswerForm()
	ctx={'que':que.que,'form':form	}
	return render_to_response("answer.html",ctx,context_instance=RequestContext(request))


@login_required
def question(request):
	id1=request.GET.get('id')
	que=models.Question.objects.get(queid=id1)
	q_name=models.MyUser.objects.get(username=que.email)
	qname=str(q_name.first_name)+" "+q_name.last_name
	obj=models.Answer.objects.filter(queid=id1)
	answer_name=[]
	for a in obj:
		name_obj=models.MyUser.objects.get(username=a.email)
		namestr=str(name_obj.first_name)+" "+name_obj.last_name
		aname_obj=(a,namestr)
		answer_name.append(aname_obj)
	ctx={'obj':answer_name,'que':que,'qname':qname}
	return render_to_response("question.html",ctx,context_instance=RequestContext(request))


@login_required
def profile_view(request):
	user_mail=request.user
	userobj=models.MyUser.objects.get(username=request.user)
	user_pro=models.User_Profile.objects.get(mid=user_mail)
	print(user_pro)
	ctx={'userobj':userobj,'user_pro':user_pro}
	return render_to_response("profile.html",ctx,context_instance=RequestContext(request))


def notification(request):
	obj=models.Question.objects.filter(email=request.user)
	page=request.GET.get('page')
	p=Paginator(obj,'5')
	try:
		page=int(request.GET.get('page','1'))
	except ValueError:
		page=1
	try:
		pobj=p.page(page)
	except InvalidPage:
		pobj=p.page(p.num_pages)
	Notificationlist=[]
	cnt=0
	for q in pobj:
		try:
			a_obj=models.Answer.objects.filter(queid=q.queid).order_by('-date_answered')
		except IndexError:
			a_obj=""
		sector=q.sector.all()
		for a in a_obj:
			user_name=models.MyUser.objects.get(username=a.email)
			ans=[q,sector,a,str(user_name.first_name)+" "+user_name.last_name]
			cnt=cnt+1
			Notificationlist.append(ans)
	print(request.user)
	userpro=models.User_Profile.objects.get(mid=request.user)
	ncnt=userpro.notification_count
	pending=cnt-ncnt
	userpro.notification_count=cnt
	userpro.save()
	ctx={'Notify':Notificationlist,'Ncnt':pending}
	return render_to_response("notifications.html",ctx,context_instance=RequestContext(request))

	
def question_uploaded(request):
	ctx={}
	return render_to_response("Question_uploaded.html",ctx,context_instance=RequestContext(request))

def about(request):
	ctx={}
	return render_to_response("about.html",ctx,context_instance=RequestContext(request))

@login_required
def sec_wise_disp(request):
	sec_obj=models.Sector.objects.all()
	obj=models.Question.objects.filter(sector=request.GET.get('sectornm'))
	page=request.GET.get('page')
	p=Paginator(obj,'5')
	try:
		page=int(request.GET.get('page','1'))
	except ValueError:
		page=1
	try:
		pobj=p.page(page)
	except InvalidPage:
		pobj=p.page(p.num_pages)
	qalist=[]
	for q in pobj:
		try:
			aobj=models.Answer.objects.filter(queid=q.queid).order_by('-date_answered').__getitem__(0)
		except IndexError:
			aobj=""
		user_name=models.MyUser.objects.get(username=q.email)
		try:
			answerer_name=models.MyUser.objects.get(username=aobj.email)
		except:
			answerer_name=""
		try:
			ansnm=str(answerer_name.first_name)+" "+answerer_name.last_name
		except:
			ansnm=""
		sector=q.sector.all()
		a=[q,aobj,sector,(str(user_name.first_name)+" "+user_name.last_name),ansnm]
		qalist.append(a)
	ctx={'obj':qalist,'page':pobj,'sec_obj':sec_obj}
	return render_to_response('sectorwise.html',ctx,context_instance=RequestContext(request))


def notification(request):
	obj=models.Notification.objects.filter(user_ref=request.user).order_by('-datetime')
	for i in obj:
		print("Notification",i," que user:",i.ans_ref.queid.email)
	ctx={'notify':obj}
	return render_to_response("notification.html",ctx,context_instance=RequestContext(request))
