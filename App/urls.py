from django.urls import path
from . import views 
# from django.conf.urls import url

urlpatterns = [
    
    path('',views.homepage,name = "homepage"),
    path('register/', views.register,name='register' ),
    path('login/', views.user_login, name='login'),
    path('checkLogin/', views.checkLogin, name = "checkLogin"),
    path('checkSignup/', views.checkSignup,name = 'checkSignup'),
    path('checkipn/', views.checkipn,name = 'checkipn'),
    path('checkname/', views.checkname,name = 'checkname'),
    path('logout/', views.user_logout,name = 'logout'),
    path('showLogin/', views.show_login,name = 'showLogin'),
    path('showRegister/', views.show_register,name = 'showRegister'),
    path('uploadBill/', views.uploadBill,name = 'uploadBill'),
    path('getBill/', views.getBill,name = 'getBill'),
    path('uploadBillInsurance/', views.uploadBillInsurance,name = 'uploadBillInsurance'),
    path('createPolicy/', views.createPolicy,name = 'createPolicy'),
    path('policies/', views.policies,name = 'policies'),
     path('getPolicy/', views.getPolicy,name = 'getPolicy'),
     path('contact/', views.contact,name = 'contact'),
     path('claim/', views.claim,name = 'claim'),
     path('checkFraud/', views.checkFraud, name='checkFraud'),
]