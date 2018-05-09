from django.shortcuts import render
from django.views.decorators import csrf
from WebDemo.models import Test

# 表格后面还有一个{% csrf_token %}的标签。csrf 全称是 Cross Site Request Forgery。
# 这是Django提供的防止伪装提交请求的功能。POST 方法提交的表格，必须有此标签


def search_post(request):
    ctx = {}
    if request.POST:
        searchstr = request.POST['q']
        ctx['rlt'] = searchstr

        testlist = Test.objects.filter(name=searchstr)
        ctx['testlist'] = testlist

    return render(request, "post.html", ctx)


