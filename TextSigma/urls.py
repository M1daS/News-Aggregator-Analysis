from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^$', views.text_homepage, name = 'text_homepage'),
	url(r'^SumDisp/', views.sumdisp, name = 'sumdisp'),

]