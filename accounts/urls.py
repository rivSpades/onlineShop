from django.urls import path
from . import  views


app_name = 'accounts'

urlpatterns=[

    path('register',views.RegisterAPIView.as_view(),name='register'),
    path('login',views.LoginAPIView.as_view(),name='login'),
    path('logout',views.LogoutAPIView.as_view(),name='logout'),
    path('activate/<uidb64>/<token>',views.ActivateAccountAPIView.as_view(),name='activate_account'),
    path('reset_password/<uidb64>/<token>',views.ResetPasswordAPIView.as_view(),name='reset_password'),
    path('dashboard',views.DashboardView.as_view(),name='dashboard'),
    path('forgot_password',views.ForgotPasswordAPIView.as_view(),name='forgot_password'),
    path('validate_token', views.ValidateTokenAPIView.as_view(), name='validate_token'),

]