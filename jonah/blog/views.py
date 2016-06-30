from django.shortcuts import render
from blog.util import Constant
from django.http import HttpResponseRedirect
import logging
# Create your views here.
def index(request):
    context = {}
    context['name'] = Constant.BLOG_NAME
    context['desc'] = Constant.BLOG_DESC
    if Constant.SESSION_KEY in request.COOKIES:
        context['username'] = request.COOKIES[Constant.SESSION_KEY]
    return render(request,'index.html',context)
#login
def login(request):
    if request.method == "POST":
        if 'username' in request.POST and 'password' in request.POST:
            un = request.POST['username']
            pw = request.POST['password']
            '''校验账号密码'''
            if un == Constant.USERNAME and pw == Constant.PASSWORD:
                #save session
                request.session['username'] = un
                request.session['password'] = pw
                context = {}
                context['name'] = Constant.BLOG_NAME
                context['desc'] = Constant.BLOG_DESC
                context['username'] = un
                response = render(request,'index.html',context)
                if 'remember' in request.POST and request.POST['remember'] == 'remember-me':
                    response.set_cookie(Constant.SESSION_KEY, un,max_age=1000*60*60*24*30)
                else:
                    response.delete_cookie(Constant.SESSION_KEY)
                return response
            else:
                context = {}
                context['message'] = '账号或密码错误'
                return  render(request,'login.html',context)
    #del session
    if request.method == "GET" and 'out' in request.GET:
        context = {}
        context['name'] = Constant.BLOG_NAME
        context['desc'] = Constant.BLOG_DESC
        response = render(request,'index.html',context)
        if 'username' in request.session:
            del request.session['username']
            response.delete_cookie(Constant.SESSION_KEY)
        return response
        #return render(request,'index.html',context)
    return render(request,'login.html')