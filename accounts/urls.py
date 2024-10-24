from django.urls import path
from . import  views


app_name = 'accounts'

urlpatterns=[

    path('register',views.RegisterView.as_view(),name='register'),
    path('login',views.LoginView.as_view(),name='login'),
    path('logout',views.LogoutView.as_view(),name='logout'),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate_account'),
    path('reset_password/<uidb64>/<token>',views.ResetPasswordView.as_view(),name='reset_password'),
    path('dashboard',views.DashboardView.as_view(),name='dashboard'),
    path('forgot_password',views.ForgotPasswordView.as_view(),name='forgot_password'),

]