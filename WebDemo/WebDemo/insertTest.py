from django.shortcuts import render
from datetime import datetime
from WebDemo.models import Test
from django.http import HttpResponse

# Create your views here.


def insert_test(request):
    rdtime = datetime.now()
    print(rdtime)
    test1 = Test(name="测试账号", recdate=rdtime)
    test1.save()
    return HttpResponse("<p>数据添加成功！</p>")
