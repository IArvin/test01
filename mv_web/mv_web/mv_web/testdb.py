# -*-coding: utf-8-*-
from django.http import HttpResponse
from testmodel.models import test


# 数据库操作
def testdb(request):
    test1 = test(name="hello")
    test1.save()
    return HttpResponse('<p>insert hello in to testdb success!</p>')