"""project8 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from manageStore.views import *

urlpatterns = [
    path('', add_data_source),
    path('login/', loginPage,name='login'),
    # path('register/', registerPage, name='register'),
    path('logout/', logoutUser, name="logout"),
    path('add_user/', registerPage, name='add_user'),
    path('delete/<int:id>', destroy_user),
    path('edit/<int:id>', edit_user), 
    path('update/<int:id>', update_user),


    # ==============>start Path data resource<=====================
    path('addDataSource/', addDataSource, name='addDataSource'),
    path('editDataSource/<id>', editDataSource , name="editDataSource"),
    path('updateDataSource', updateDataSource , name="updateDataSource"),
    path('deleteData/<id>', deleteData , name="deleteData"),
  # ==============>end Path data resource<=======================


  # ==============>start Path mange source<=======================
    path('manage_store/', manage_store, name='manage_store'),
    path('manage_store/upload', upload, name='upload'),
    path('manage_store/upload', index, name='index'),
    path('manage_store/<int:id>', information, name='information'),
    path('information/', information, name='information'),
  # ==============>end Path mange source<=======================
]
