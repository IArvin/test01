# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


# Create your models here.

class mv_msg(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name=id)
    movie_name = models.CharField(max_length=100, verbose_name=(u"movie_name"))
    new_name = models.CharField(max_length=100, verbose_name=(u"new_name"))
    origin = models.CharField(max_length=100, verbose_name=(u"origin"))
    image = models.CharField(max_length=200, verbose_name=(u"image"))
    # origin_year = models.CharField(max_length=4, verbose_name=(u"origin_year"))
    movie_time = models.CharField(max_length=100, verbose_name=(u"movie_time"))
    movie_type = models.CharField(max_length=100, verbose_name=(u"movie_type"))
    link_msg = models.CharField(max_length=200, verbose_name=(u"link_msg"))
    movie_url = models.CharField(max_length=200, verbose_name=(u"movie_url"))
