from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from django.views.decorators.cache import cache_control
from django.http import HttpResponse,HttpResponseRedirect
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
from django.contrib.auth import authenticate,login,logout
from models import book
import os,tempfile
from hashlib import sha1
from django.db.models import Q

def index(request):
	books=book.objects.all()[:10]
	return render_to_response("home.html",{'title':'Bookshelf','books':books})
def search(request):
	key=request.GET['key']
	b=book.objects.filter(Q(author__icontains=key) | Q(title__icontains=key))
	return render_to_response('search.html',{'books':b})

def details(request,key):
	b=book.objects.filter(bookKey=key)
	if b:
		return render_to_response('bookDetails.html',{'book':b[0]})
	else:
		return HttpResponseRedirect('/')

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def upload(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')
	if request.method=='POST':
		l=request.FILES['file']
		title=request.POST['title']
		author=request.POST['author']
		if l and title and author and l.content_type == 'application/pdf':
			key=sha1(title+author).hexdigest()[:15]
			if key in os.listdir(settings.BOOKS):
				return HttpResponseRedirect('/upload')
			b=book(title=title,author=author,bookKey=key)
			b.save()
			move_uploaded_file(l,key)
			createThumbnail(key)
			return HttpResponseRedirect('/upload')
		else:
			return render_to_response("upload.html",
			{'error':'1.All fields are mandatory<br>2.Only PDF files Allowed'},context_instance=RequestContext(request))
	else:
		return render_to_response("upload.html",{'title':'Upload files'},context_instance=RequestContext(request))
	
def move_uploaded_file(f,key):
	d=settings.BOOKS
	destination = open(d+key,'wb+')
	for chunk in f.chunks():
		destination.write(chunk)
	destination.close()
	return
def createThumbnail(key):
	file_loc=settings.BOOKS+key+'[0]'
	img_loc=settings.MEDIA_ROOT+key+'.jpg'
	os.system("convert -quality 50 -density 600x600 %s %s"%(file_loc,img_loc))
	return

def download(request,key):
	file_loc=settings.BOOKS+key
	w=FileWrapper(file(file_loc))
	response = HttpResponse(w,mimetype='text/plain')
	response['Content-Disposition'] = "attachment; filename=%s.pdf"%(key)
	return response

def userLogin(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/upload/')
	elif request.method=='GET':
		return render_to_response("login.html",context_instance=RequestContext(request))
	else:
		user=authenticate(username=request.POST['uname'],password=request.POST['passwd'])
		if user is not None:
			login(request,user)
			return HttpResponseRedirect('/upload/')
	return HttpResponseRedirect('/')

def userLogout(request):
	logout(request)
	return HttpResponseRedirect('/')
