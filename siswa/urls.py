from django.urls import path

from . import views

app_name = 'siswa'
urlpatterns = [
    path('', views.index, name='index'),
    path('absensi/', views.absensi, name='absensi'),
    path('absensi/submit/', views.submit, name='submit'),
    path('absensi/submit/proses/', views.proses_submit, name='proses_submit'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.editprofile, name='edit_profile'),
    path('logout/', views.logout, name='logout'), 
]