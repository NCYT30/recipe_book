"""
URL configuration for recipe_book project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name = 'home'),
    path('base/', views.base, name = 'base'),
    path('recipe/', views.recipe_page, name = 'recipe'),
    path('recipe/create/', views.create_recipe, name = 'recipe_create'),
    path('category/', views.category, name = 'category'),
    path('saurce/<int:id>/', views.saurce, name = 'saurce'),
    path('recipe/<int:id>/rate/', views.rate_recipe, name = 'rate-recipe'),
    path('top/', views.top, name = 'top'),
    path('chatbot-response/', views.chatbot_response, name='chatbot_response'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
