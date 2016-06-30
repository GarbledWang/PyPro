from django.shortcuts import render
from blog.util import Constant
# Create your views here.
def index(request):
    context = {}
    context['name'] = Constant.BLOG_NAME
    context['desc'] = Constant.BLOG_DESC
    return render(request,'index.html',context)