from django.urls import path

from . import views

app_name = 'guru'
urlpatterns = [
    path('', views.index, name='index'),
    path('siswa/', views.kelas, name='kelas'),
    path('siswa/kelas/', views.siswa, name='siswa'),
    path('absensi/', views.kelasAbsensi, name='kelas_absensi'),
    path('absensi/kelas/', views.absensi, name='absensi'),
    path('absensi/kelas/tambah/', views.tambah_absensi, name='tambah_absensi'),
    path('absensi/kelas/tambah/proses/', views.proses_tambahAbsensi, name='proses_tambah_absensi'),
    path('absensi/kelas/edit/', views.edit_absensi, name='edit_absensi'),
    path('absensi/kelas/edit/proses/', views.proses_edit_absensi, name='proses_edit_absensi'),
    path('absensi/kelas/hapus/', views.hapus_absensi, name='hapus_absensi'),
    path('laporan/lihat/', views.lihat_laporan, name='lihat_laporan'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.editprofile, name='edit_profile'),
]