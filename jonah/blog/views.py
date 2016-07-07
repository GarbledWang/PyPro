from django.shortcuts import render
from blog.util import Constant
from blog.models import Article,User
from django.http import HttpResponseRedirect
import time


# Create your views here.
def index(request):
    context = {}
    context['name'] = Constant.BLOG_NAME
    context['desc'] = Constant.BLOG_DESC
    if Constant.SESSION_KEY in request.COOKIES:
        context['username'] = request.COOKIES[Constant.SESSION_KEY]
    if 'username' in request.session:
        context['username'] = request.session['username']
    if Constant.SESSION_KEY in request.COOKIES or 'username' in request.session:
        un = context['username']
        all_article = Article.objects.all().filter(author=un)
        context['article'] = all_article
        print(all_article)
    return render(request  ,'index.html',context)


#login
def login(request):
    if request.method == "POST":
        if Constant.SESSION_KEY in request.POST and 'password' in request.POST:
            un = request.POST['username']
            pw = request.POST['password']
            '''校验账号密码'''
            user = User.objects.filter(username=un,password=pw)
            if user:
                #save session
                request.session['username'] = un
                request.session['password'] = pw
                response = HttpResponseRedirect('/')
                if 'remember' in request.POST and request.POST['remember'] == 'remember-me':
                    response.delete_cookie(Constant.COOKIE_KEY)
                    response.set_cookie(Constant.COOKIE_KEY, un,max_age=1000*60*60*24*30)
                else:
                    response.delete_cookie(Constant.COOKIE_KEY)
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
        response = HttpResponseRedirect('/')
        if 'username' in request.session:
            del request.session['username']
            response.delete_cookie(Constant.COOKIE_KEY)
        return response
    return render(request,'login.html')


#edit article
def edit(request):
    if request.method == 'GET':
        if 'arid' in request.GET:
            context = {}
            arid = request.GET['arid']
            article = Article.objects.filter(id=arid)[0]
            context['art'] = article
            return render(request,'edit.html',context)
        elif 'username' in request.session:
            context = {}
            context['name'] = Constant.BLOG_NAME
            return render(request,'edit.html',context)
        else:
            return HttpResponseRedirect('/')
    else:#POST commit
        if 'id' in request.POST:
            article = Article.objects.get(id=request.POST['id'])
            article.title = request.POST['title']
            article.content = request.POST['content']
            article.save()
            return HttpResponseRedirect('/')
        else:
            un = _get_name(request)
            article = Article(title=request.POST['title'] ,author=un,date=time.strftime('%Y-%m-%d',time.localtime(time.time())),content=request.POST['content'])
            article.save()
            return HttpResponseRedirect('/')


#显示页面
def show(request):
    if request.method == "GET" and 'article' in request.GET:
        un = _get_name(request)
        if un:
            _id = request.GET['article']
            article = Article.objects.filter(id=_id)[0]
            context = {}
            context['name'] = un
            context['art'] = article
            return render(request,'show.html',context)


def _get_name(request):
    un = None
    if Constant.SESSION_KEY in request.COOKIES:
        un = request.COOKIES[Constant.SESSION_KEY]
    if 'username' in request.session:
        un = request.session['username']
    return un


#register
def register(request):
    if request.method == 'POST':
        if Constant.SESSION_KEY in request.POST and 'password' in request.POST:
            un = request.POST['username']
            pw = request.POST['password']
            user = User.objects.filter(username=un)
            if user:
                context = {}
                context['message'] = '用户名已存在'
                return render(request,'register.html',context)
            request.session['username'] = un
            #save user
            user = User(username=un,password=pw)
            user.save()
            return HttpResponseRedirect('/')
    else:
        return render(request,'register.html')
