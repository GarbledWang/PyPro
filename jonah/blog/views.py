from django.shortcuts import render
from blog.util import Constant
# Create your views here.
def index(request):
    context = {}
    context['name'] = Constant.BLOG_NAME
    context['desc'] = Constant.BLOG_DESC
    return render(request,'index.html',context)

def login(request):
    if request.method == "POST":
        if 'username' in request.POST and 'password' in request.POST:
            un = request.POST['username']
            pw = request.POST['password']
            '''校验账号密码'''
            if un == "jonah" and pw == '5442377':
                #save session
                request.session['username'] = un
                request.session['password'] = pw
                context = {}
                context['name'] = Constant.BLOG_NAME
                context['desc'] = Constant.BLOG_DESC
                context['username'] = un
                return render(request,'index.html',context)
        else:
            context = {}
            context['message'] = '账号或密码错误'
            return  render(request,'login.html',context)
    return render(request,'login.html')