"""showweixin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from show import views

urlpatterns = [
    url(r'^pre_solve/$',views.page_pre_solve,name='page_pre_solve'),
    url(r'^processing/$',views.pre_solve,name="pre_solve"),
    url(r'^$',views.show_keywords,name='show_keywords'),
    url(r'^finish/$',views.finish,name='finish'),
    url(r'^keywordpassage/(?P<page1>[0-9]+)/$',views.show_keyword_passage,name="show_keyword_passage"),
    url(r'^passage_detail/(?P<page>[0-9]+)/$',views.passage_detail,name='passage_detail'),
    url(r'^passage_all_analyse/$',views.passage_all_analyse,name='passage_all_analyse'),  #总体分析  公众号总数、所有公众号发文章总数、所有文章总点赞数、总阅读数
    url(r'^passage_part_analyse/$',views.passage_part_analyse,name='passage_part_analyse'),  #局部分析  发文最多的前20个公众号、点赞数最多的前20个公众号、最活跃的前20个公众号
    url(r'^tophot/$',views.tophot,name='tophot'),  #局部分析   最火的公众号、文章
    url(r'^huitu/$',views.huitu,name='huitu'),    #绘制发文趋势图
    url(r'^related/$',views.releated,name='related'),    #计算相关度
    url(r'^related_sort/$',views.related_sort,name='related_sort'), #根据每个热词的相关度进行排序
]
