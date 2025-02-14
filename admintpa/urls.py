from django.urls import path

from . import views

app_name = 'admintpa'
urlpatterns = [
    path('', views.index, name='index'),
    path('siswa/', views.siswa, name='siswa'),
    path('siswa/tambah/', views.tambah_siswa, name='tambah_siswa'),
    path('siswa/edit/', views.edit_siswa, name='edit_siswa'),
    path('siswa/edit/proses/', views.proses_edit_siswa, name='proses_edit_siswa'),
    path('siswa/hapus/', views.hapus_siswa, name='hapus_siswa'),
    path('guru/', views.guru, name='guru'),
    path('guru/tambah/', views.tambah_guru, name='tambah_guru'),
    path('guru/edit/', views.edit_guru, name='edit_guru'),
    path('guru/edit/proses/', views.proses_edit_guru, name='proses_edit_guru'),
    path('guru/hapus/', views.hapus_guru, name='hapus_guru'),
    path('kelas/', views.kelas, name='kelas'),
    path('kelas/tambah/', views.tambah_kelas, name='tambah_kelas'),
    path('kelas/detail/', views.detail_kelas, name='detail_kelas'),
    path('kelas/detail/tambah-agtkelas/', views.tambah_agtkelas, name='tambah-agtkelas'),
    path('kelas/detail/tambah-agtkelas/proses/', views.proses_tambah_agtkelas, name='proses_tambah_agtkelas'),
    path('kelas/detail/hapus-agtkelas/', views.hapus_agtkelas, name='hapus-agtkelas'),
    path('kelas/edit/', views.edit_kelas, name='edit_kelas'),
    path('kelas/edit/proses/', views.proses_edit_kelas, name='proses_edit_kelas'),
    path('kelas/hapus/', views.hapus_kelas, name='hapus_kelas'),
    path('mapel/', views.mapel, name='mapel'),
    path('mapel/tambah/', views.tambah_mapel, name='edit_mapel'),
    path('mapel/edit/', views.edit_mapel, name='edit_mapel'),
    path('mapel/edit/proses/', views.proses_edit_mapel, name='proses_edit_mapel'),
    path('mapel/hapus/', views.hapus_mapel, name='hapus_mapel'),
    path('laporan/', views.laporan, name='laporan'),
    path('laporan/lihat/', views.laporan_kelas, name='laporan_kelas'),
    # path('laporan/kelas2/', views.laporan_kelas2, name='laporan_kelas2'),
    # path('laporan/kelas3/', views.laporan_kelas3, name='laporan_kelas3'),
]