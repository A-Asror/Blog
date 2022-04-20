from django.contrib import admin
from .models import Category, PhotoPost, VideoPost, Article, Comments, SubComments, Photos

admin.site.register((Category, VideoPost, PhotoPost, Article, Comments, SubComments, Photos))
# admin.site.register(CReate_Video)
