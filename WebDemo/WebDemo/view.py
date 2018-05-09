from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from WebDemo.models import Test
# Create your views here.


def hello(request):
    contex = {"hello": "Hello XX！", "title": "Django Demo",
              "dt": datetime.now().strftime("%H:%M:%S"),
              "tdt": datetime.today()}

    testlist = Test.objects.all().order_by("recdate")
    contex["testlist"] = testlist
    return render(request, 'hello.html', contex)
