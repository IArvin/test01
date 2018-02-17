# -*-coding: utf-8-*-
from django.http import HttpResponse
from movie_model.models import mv_msg


# 数据库操作
def movie_db(request):
    response1 = ""

    response1 = mv_msg.objects.get(id=128)
    print response1.image
    response = response1.image
    return HttpResponse("<p>"+response+"</p>")