"""anki_th_web_app_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from card_generator import views

urlpatterns = [
    path('admin/'      , admin.site.urls),
    path(''            , views.home_page),
    path('home/'       , views.stream_response),
    path('guide/'      , views.guide_page),
    path('try_it/'     , views.try_it_page),
    path('shared_deck/', views.shared_deck_page),
]
