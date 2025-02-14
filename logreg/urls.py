from django.urls import path

from . import views

app_name = 'logreg'
urlpatterns = [
    path('', views.login, name='login_form'),
    path('proses', views.proses_login, name='proses_login'),
    path('logout', views.logout, name='logout'),
]