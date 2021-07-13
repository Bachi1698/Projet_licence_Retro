from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('is_deconnexion', views.login, name='logout'),
    path('account_confirm/<slug:uidb64>/<slug:token>/',views.activate,name="account_confirm_email"),#### route de confirmation du mail


]