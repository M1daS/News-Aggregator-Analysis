from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^$', views.news_homepage, name = 'news_homepage'),
	url(r'^Summary/', views.get_summary, name = 'get_summary'),
	url(r'^Organize/', views.organize_articles, name = 'organize_articles'),
	url(r'^TrendingTopic/', views.trending_topic, name = 'trending_topic'),
	url(r'^Tree/', views.newstree, name = 'tree'),
	url(r'^Graphics/', views.graphics, name = 'graphics'),
	url(r'^concensus/', views.concensus, name = 'concensus'),
]