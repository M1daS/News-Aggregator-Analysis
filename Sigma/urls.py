

from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin

from django.conf.urls import url
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.sigma_homepage, name = 'sigma_homepage'),

	url(r'^News/', include('NewsSigma.urls')),
	url(r'^Text/', include('TextSigma.urls')),


	url(r'^Signup/', views.signup, name = 'signup'),
    url(r'^Login/$', auth_views.login, {'template_name': 'login.html'}),
    url(r'^Logout/$', auth_views.logout, {'template_name': 'logout.html'}),
]


