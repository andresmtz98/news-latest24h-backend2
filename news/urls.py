from django.conf.urls import url
from news.views import *

app_name = 'articles'
urlpatterns = [
    url(r'^articles/$', ArticleList.as_view(), name='articles')
]