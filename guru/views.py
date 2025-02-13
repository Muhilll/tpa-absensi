from django.shortcuts import render, redirect
import os
from django.conf import settings
import shutil
from admintpa.models import Kelas, Agtkelas, User, Mapel, Absensi, Kehadiran

# Create your views here.

def index(request):
    id_user = request.session.get('id_user')
    kelas = Kelas.objects.get(id_user = id_user)

    jml_agtkelas = Agtkelas.objects.filter(id_kelas=kelas.id).count()

    query = """
        SELECT admintpa_user.* 
        FROM admintpa_user
        INNER JOIN admintpa_agtkelas ON admintpa_user.id = admintpa_agtkelas.id_user
        WHERE admintpa_agtkelas.id_kelas = %s LIMIT 10
    """
    user = User.objects.raw(query, [kelas.id])

    query = """
        SELECT admintpa_kehadiran.id AS id,
                admintpa_absensi.tanggal AS tanggal_absensi, 
                admintpa_kelas.nama AS nama_kelas, 
                admintpa_mapel.nama AS nama_mapel, 
                admintpa_user.nama AS nama_user, 
                admintpa_kehadiran.keterangan AS keterangan_kehadiran
            FROM admintpa_absensi
            INNER JOIN admintpa_kelas ON admintpa_absensi.id_kelas = admintpa_kelas.id
            INNER JOIN admintpa_mapel ON admintpa_absensi.id_mapel = admintpa_mapel.id
            INNER JOIN admintpa_kehadiran ON admintpa_absensi.id = admintpa_kehadiran.id_absensi
            INNER JOIN admintpa_agtkelas ON admintpa_kehadiran.id_agtkelas = admintpa_agtkelas.id
            INNER JOIN admintpa_user ON admintpa_agtkelas.id_user = admintpa_user.id where admintpa_kelas.id = %s
            ORDER BY admintpa_absensi.tanggal DESC
            LIMIT 10
    """
    kehadiran = Kehadiran.objects.raw(query, [kelas.id])

    return render(request, 'home_guru/index.html', {
        'jml_agtkelas': jml_agtkelas,
        'user': user,
        'kehadiran': kehadiran,
    })

def siswa(request):
    id_user = request.session.get('id_user')
    kelas = Kelas.objects.get(id_user = id_user)
    query = """
        SELECT admintpa_user.* 
        FROM admintpa_user
        INNER JOIN admintpa_agtkelas ON admintpa_user.id = admintpa_agtkelas.id_user
        WHERE admintpa_agtkelas.id_kelas = %s
    """
    agtkelas = User.objects.raw(query, [kelas.id])  
    return render(request, 'siswa_guru/index.html', {'agtkelas': agtkelas})

def absensi(request):
    id_user = request.session.get('id_user')
    kelas = Kelas.objects.get(id_user=id_user)
    query = """SELECT admintpa_absensi.id as id, admintpa_mapel.nama as mapel, 
        admintpa_absensi.nama, admintpa_absensi.tanggal, 
        admintpa_absensi.des FROM admintpa_absensi INNER JOIN admintpa_mapel on admintpa_absensi.id_mapel = admintpa_mapel.id 
        WHERE admintpa_absensi.id_kelas = %s
    """
    absensi = Absensi.objects.raw(query, [kelas.id])
    return render(request, 'absensi_guru/index.html', {'absensi': absensi})

def tambah_absensi(request):
    id_user = request.session.get('id_user')
    kelas = Kelas.objects.get(id_user=id_user)
    mapel = Mapel.objects.all()

    if request.method == 'POST':
        Absensi.objects.create(
            id_kelas=kelas.id,
            id_mapel=request.POST['id_mapel'],
            nama=request.POST['nama'],
            tanggal=request.POST['tanggal'],
            des=request.POST['des'],
        )
        return redirect('/guru/absensi')
    
    return render(request, 'absensi_guru/tambah.html', {'mapel': mapel})

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
    id_user = request.session.get('id_user')
    kelas = Kelas.objects.get(id_user=id_user)
    absensi = Absensi.objects.get(id = request.POST['id_absensi'])
    absensi.id_kelas = kelas.id
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

def laporan(request):
    id_user = request.session.get('id_user')
    kelas = Kelas.objects.get(id_user=id_user)
    query = """SELECT admintpa_absensi.id as id, admintpa_mapel.nama as mapel, 
        admintpa_absensi.nama, admintpa_absensi.tanggal, 
        admintpa_absensi.des FROM admintpa_absensi INNER JOIN admintpa_mapel on admintpa_absensi.id_mapel = admintpa_mapel.id 
        WHERE admintpa_absensi.id_kelas = %s
    """
    absensi = Absensi.objects.raw(query, [kelas.id])
    return render(request, 'laporan_guru/index.html', {'absensi': absensi})

def lihat_laporan(request):
    id_absensi = request.POST['id_absensi']
    id_user = request.session.get('id_user')
    kelas = Kelas.objects.get(id_user=id_user)
    
    query = """
    SELECT admintpa_kehadiran.id AS id,
           admintpa_absensi.tanggal AS tanggal_absensi, 
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
    dtkelas = Kelas.objects.get(id=kelas.id)
    return render(request, 'laporan_guru/lihat.html', {'kehadiran': kehadiran, 'kelas': dtkelas})

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