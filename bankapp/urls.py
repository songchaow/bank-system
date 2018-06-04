"""bank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('subbank/',views.subbank,name='subbank'),
    path('subbank/subbanksearch',views.subbank_list,name='subbanksearch'),
    path('subbank/edit',views.subbank_edit,name='subbankedit'),
    path('subbank/delete/<int:pk>',views.SubBankDeleteView.as_view()),
    path('staff',views.StaffIndexView.as_view()),
    path('staff/search',views.StaffListView.as_view()),
    #path('staff/edit',views.StaffEditView.as_view())
    path('staff/edit/<int:pk>',views.StaffEditViewnew.as_view()),
    path('staff/create',views.StaffCreateView.as_view()),
    path('staff/delete/<int:pk>',views.StaffDeleteView.as_view()),
    path('customer/',views.CustomerIndexView.as_view()),
    path('customer/search',views.CustomerListView.as_view()),
    path('customer/edit/<int:pk>',views.CustomerUpdateView.as_view()),
    path('customer/create',views.CustomerCreateView.as_view()),
    path('customer/delete/<int:pk>',views.CustomerDeleteView.as_view()),
    path('account',views.AccountIndexView.as_view()),
    path('account/search',views.AccountSearchView.as_view()),
    path('account/delete/storage/<int:pk>',views.SAccountDeleteView.as_view()),
    path('account/storage/create',views.SAccountCreateView.as_view()),
    path('account/check/create',views.CAccountCreateView.as_view()),
    path('account/edit/storage/<int:pk>',views.SAccountUpdateView.as_view()),
    path('account/edit/check/<int:pk>',views.CAccountUpdateView.as_view()),
    path('loan',views.LoanIndexView.as_view()),
    path('loan/create',views.LoanCreateView.as_view()),
    path('loan/<int:pk>/payrecord',views.PayRecordListView.as_view()),
    path('loan/<int:pk>/createpayrecord',views.PayRecordCreateView.as_view()),
    path('loan/<int:pk>/delete',views.LoanDeleteView.as_view())
]
