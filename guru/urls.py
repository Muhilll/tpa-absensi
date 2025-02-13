from django.urls import path

from . import views

app_name = 'guru'
urlpatterns = [
    path('', views.index, name='index'),
    path('siswa/', views.siswa, name='siswa'),
    path('absensi/', views.absensi, name='absensi'),
    path('absensi/tambah/', views.tambah_absensi, name='tambah_absensi'),
    path('absensi/edit/', views.edit_absensi, name='edit_absensi'),
    path('absensi/edit/proses/', views.proses_edit_absensi, name='proses_edit_absensi'),
    path('absensi/hapus/', views.hapus_absensi, name='hapus_absensi'),
    path('laporan/', views.laporan, name='laporan'),
    path('laporan/lihat/', views.lihat_laporan, name='lihat_laporan'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.editprofile, name='edit_profile'),
]