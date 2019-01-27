"""demosite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.urls import path
from first import views
from second import views as views2
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page, name='home'),
    path('calc/', views.calculator_page, name='calc'),
    path('squadequal/', views.squadEqual, name='squadEqual'),
    path('idk/', views2.index_page),
    path('riddle/', views.riddle),
    path('answer/', views.answer),
    path('menu/', views.menu_page),
    path('multiply/', views.multiply_page),
    path('str2words/', views.str2words),
    path('str_history/', views.str_history),

    path('login/', auth_views.LoginView.as_view()),
    path('logout/', auth_views.LogoutView.as_view()),
    path('signup/', views.signup),
]
