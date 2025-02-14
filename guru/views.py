from django.shortcuts import render, redirect
import os
from django.conf import settings
import shutil
from django.utils.timezone import localtime
from datetime import datetime
from admintpa.models import Kelas, Agtkelas, User, Mapel, Absensi, Kehadiran


# Create your views here.

def index(request):
    id_user = request.session.get('id_user')

    query = """
        SELECT COUNT(admintpa_agtkelas.id) as jml_agtkelas FROM admintpa_kelas 
        INNER JOIN admintpa_agtkelas on admintpa_kelas.id = admintpa_agtkelas.id_kelas 
        WHERE admintpa_kelas.id_user = %s
    """

    jml_agtkelas = Agtkelas.objects.filter(id_kelas__in=Kelas.objects.filter(id_user=id_user)).count()

    dtkelas = Kelas.objects.filter(id_user = id_user)

    query = """
        SELECT admintpa_kehadiran.id AS id,
                admintpa_absensi.tanggal AS tanggal_absensi, 
                admintpa_kehadiran.jam, 
                admintpa_kelas.nama AS nama_kelas, 
                admintpa_mapel.nama AS nama_mapel, 
                admintpa_user.nama AS nama_user, 
                admintpa_kehadiran.keterangan AS keterangan_kehadiran
            FROM admintpa_absensi
            INNER JOIN admintpa_kelas ON admintpa_absensi.id_kelas = admintpa_kelas.id
            INNER JOIN admintpa_mapel ON admintpa_absensi.id_mapel = admintpa_mapel.id
            INNER JOIN admintpa_kehadiran ON admintpa_absensi.id = admintpa_kehadiran.id_absensi
            INNER JOIN admintpa_agtkelas ON admintpa_kehadiran.id_agtkelas = admintpa_agtkelas.id
            INNER JOIN admintpa_user ON admintpa_agtkelas.id_user = admintpa_user.id where admintpa_kelas.id_user = %s
            ORDER BY admintpa_absensi.tanggal DESC
            LIMIT 10
    """
    kehadiran = Kehadiran.objects.raw(query, [id_user])

    return render(request, 'home_guru/index.html', {
        'jml_agtkelas': jml_agtkelas,
        'dtkelas': dtkelas,
        'kehadiran': kehadiran,
    })

def kelas(request):
    id_user = request.session.get('id_user')
    kelas = Kelas.objects.filter(id_user = id_user)
    return render(request,'siswa_guru/kelas.html', {'kelas': kelas})

def siswa(request):
    id_user = request.session.get('id_user')
    id_kelas = request.POST['id_kelas']
    query = """
        SELECT admintpa_user.* 
        FROM admintpa_user
        INNER JOIN admintpa_agtkelas ON admintpa_user.id = admintpa_agtkelas.id_user
        WHERE admintpa_agtkelas.id_kelas = %s
    """
    agtkelas = User.objects.raw(query, [id_kelas])  
    return render(request, 'siswa_guru/index.html', {'agtkelas': agtkelas})

def kelasAbsensi(request):
    id_user = request.session.get('id_user')
    kelas = Kelas.objects.filter(id_user = id_user)
    return render(request,'absensi_guru/kelas.html', {'kelas': kelas})

def absensi(request):
    id_kelas = request.GET['id_kelas']
    query = """SELECT admintpa_absensi.id as id, admintpa_mapel.nama as mapel, 
        admintpa_absensi.nama, admintpa_absensi.tanggal, admintpa_absensi.mulai, admintpa_absensi.batas, 
        admintpa_absensi.des FROM admintpa_absensi INNER JOIN admintpa_mapel on admintpa_absensi.id_mapel = admintpa_mapel.id 
        WHERE admintpa_absensi.id_kelas = %s
    """
    absensi = Absensi.objects.raw(query, [id_kelas])
    return render(request, 'absensi_guru/index.html', {'absensi': absensi, 'id_kelas': id_kelas})

def tambah_absensi(request):
    id_kelas = request.POST['id_kelas']
    mapel = Mapel.objects.all()

    return render(request, 'absensi_guru/tambah.html', {'mapel': mapel, 'id_kelas': id_kelas})

def proses_tambahAbsensi(request):
    if request.method == 'POST':
        Absensi.objects.create(
            id_kelas=request.POST['id_kelas'],
            id_mapel=request.POST['id_mapel'],
            nama=request.POST['nama'],
            tanggal=datetime.strptime(request.POST['tanggal'], "%Y-%m-%d").date(),
            mulai=localtime().time(),
            batas=request.POST['batas'],
            des=request.POST['des'],
        )
        return redirect('/guru/absensi/')


def edit_absensi(request):
    id_absensi = request.POST['id_absensi']
    mapel = Mapel.objects.all()
    query = """
        SELECT admintpa_absensi.id as id, admintpa_mapel.id as id_mapel,admintpa_mapel.nama as mapel, 
            admintpa_absensi.nama, admintpa_absensi.tanggal, 
            admintpa_absensi.des FROM admintpa_absensi INNER JOIN admintpa_mapel on admintpa_absensi.id_mapel = admintpa_mapel.id 
            WHERE admintpa_absensi.id = %s
    """
    absensi = Absensi.objects.raw(query, [id_absensi])
    absensi = list(absensi)
    return render(request, 'absensi_guru/edit.html', {'absensi': absensi[0], 'mapel': mapel})

def proses_edit_absensi(request):
    absensi = Absensi.objects.get(id = request.POST['id_absensi'])
    absensi.id_mapel = request.POST['id_mapel']
    absensi.nama = request.POST['nama']
    absensi.tanggal = request.POST['tanggal']
    absensi.des = request.POST['des']
    absensi.save()

    return redirect('/guru/absensi')

def hapus_absensi(request):
    absensi = Absensi.objects.get(id = request.POST['id_absensi'])
    absensi.delete()

    return redirect('/guru/absensi')

def lihat_laporan(request):
    id_absensi = request.POST['id_absensi']
    
    query = """
    SELECT admintpa_kehadiran.id AS id,
           admintpa_absensi.tanggal AS tanggal_absensi, 
           admintpa_kehadiran.jam, 
           admintpa_kelas.nama AS nama_kelas, 
           admintpa_mapel.nama AS nama_mapel, 
           admintpa_user.nama AS nama_user, 
           admintpa_kehadiran.keterangan AS keterangan_kehadiran
    FROM admintpa_absensi
    INNER JOIN admintpa_kelas ON admintpa_absensi.id_kelas = admintpa_kelas.id
    INNER JOIN admintpa_mapel ON admintpa_absensi.id_mapel = admintpa_mapel.id
    INNER JOIN admintpa_kehadiran ON admintpa_absensi.id = admintpa_kehadiran.id_absensi
    INNER JOIN admintpa_agtkelas ON admintpa_kehadiran.id_agtkelas = admintpa_agtkelas.id
    INNER JOIN admintpa_user ON admintpa_agtkelas.id_user = admintpa_user.id
    WHERE admintpa_absensi.id = %s
    """
    
    kehadiran = Kehadiran.objects.raw(query, [id_absensi])
    dtkelas = Kelas.objects.get(id=request.POST['id_kelas'])
    return render(request, 'absensi_guru/lihat.html', {'kehadiran': kehadiran, 'kelas': dtkelas})

def profile(request):
    id_user = request.session.get('id_user')
    user = User.objects.get(id = id_user)

    return render(request, 'profile_guru/index.html', {'user': user})

def editprofile(request):
    id_user = request.session.get('id_user')
    user = User.objects.get(id = id_user)
    if request.method == 'POST':
        user.username = request.POST['username']
        user.password = request.POST.get('password', user.password)
        user.nama = request.POST['nama']
        user.tmpt_lahir = request.POST['tmpt_lahir']
        user.tgl_lahir = request.POST['tgl_lahir']
        user.jkl = request.POST['jkl']
        user.agama = request.POST['agama']
        user.alamat = request.POST['alamat']
        user.notelp = request.POST['notelp']
        if 'foto1' in request.FILES:
            if user.foto1 and os.path.exists(os.path.join(settings.MEDIA_ROOT, user.foto1.name)):
                os.remove(os.path.join(settings.MEDIA_ROOT, user.foto1.name))
            user.foto1 = request.FILES['foto1']

        if 'foto2' in request.FILES:
            if user.foto2 and os.path.exists(os.path.join(settings.MEDIA_ROOT, user.foto2.name)):
                os.remove(os.path.join(settings.MEDIA_ROOT, user.foto2.name))
            user.foto2 = request.FILES['foto2']

        if 'foto3' in request.FILES:
            if user.foto3 and os.path.exists(os.path.join(settings.MEDIA_ROOT, user.foto3.name)):
                os.remove(os.path.join(settings.MEDIA_ROOT, user.foto3.name))
            user.foto3 = request.FILES['foto3']
        user.save()
        return redirect('/guru/profile')
    else:
        return render(request, 'profile_guru/edit.html', {'user': user})