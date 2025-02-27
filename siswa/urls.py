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
    path('tes-kamera/', views.tes_kamera, name='tes_kamera'),
    path('tes-kamera/proses/', views.proses_tes_kamera, name='proses_tes_kamera'),
    path('logout/', views.logout, name='logout'), 
]   