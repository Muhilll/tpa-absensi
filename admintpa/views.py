from .models import User, Mapel, Kelas, Kehadiran, Agtkelas
import os
from django.conf import settings
import shutil
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from django.template.loader import get_template
import datetime
from xhtml2pdf import pisa
from io import BytesIO

# Create your views here.
from django.shortcuts import render, redirect

def index(request):
    jml_siswa = User.objects.filter(role = 'siswa').count()
    jml_guru = User.objects.filter(role = 'guru').count()
    jml_kelas = Kelas.objects.all().count()
    jml_admin = User.objects.filter(role = 'admin').count()
    user = User.objects.all().order_by('-id')[:10]
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
        ORDER BY admintpa_absensi.tanggal DESC
        LIMIT 10
    """
    kehadiran = Kehadiran.objects.raw(query)


    return render(request, 'home_admintpa/index.html',{
        'jml_siswa': jml_siswa,
        'jml_guru': jml_guru,
        'jml_admin': jml_admin,
        'jml_kelas': jml_kelas,
        'user': user,
        'kehadiran': kehadiran,
    })

def siswa(request):
    siswa = User.objects.filter(role = 'siswa')
    return render(request, 'siswa_admintpa/index.html', {'siswa': siswa})

def tambah_siswa(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        nama = request.POST['nama']
        tmpt_lahir = request.POST['tmpt_lahir']
        tgl_lahir = request.POST['tgl_lahir']
        jkl = request.POST['jkl']
        agama = request.POST['agama']
        alamat = request.POST['alamat']
        notelp = request.POST['notelp']
        foto1 = request.FILES['foto1']
        foto2 = request.FILES['foto2']
        foto3 = request.FILES['foto3']

        user = User.objects.filter(username = username).first()
        if user :
            messages.error(request, "Username telah ada", extra_tags="duplicateUsername")
            return redirect('/admintpa/siswa/tambah/')
        
        User.objects.create(
            username=username, 
            password=make_password(password),
            nama=nama,
            tmpt_lahir=tmpt_lahir,
            tgl_lahir=tgl_lahir,
            jkl=jkl,
            agama=agama,
            alamat=alamat,
            notelp=notelp,
            foto1=foto1,
            foto2=foto3,
            foto3=foto2,
            role="siswa",
        )
        
        return redirect('/admintpa/siswa')
    else:
        return render(request, 'siswa_admintpa/tambah.html')

def edit_siswa(request):
    siswa = User.objects.get(role = 'siswa', id = request.POST['id_siswa'])
    return render(request, 'siswa_admintpa/edit.html', {'siswa': siswa})

def proses_edit_siswa(request):
    siswa = User.objects.get(role = 'siswa', id = request.POST['id_siswa'])
    siswa.username = request.POST['username']
    password = request.POST.get('password', None)
    if password:  # Hanya hash password jika ada input baru
        siswa.password = make_password(password)
    siswa.nama = request.POST['nama']
    siswa.tmpt_lahir = request.POST['tmpt_lahir']
    siswa.tgl_lahir = request.POST['tgl_lahir']
    siswa.jkl = request.POST['jkl']
    siswa.agama = request.POST['agama']
    siswa.alamat = request.POST['alamat']
    siswa.notelp = request.POST['notelp']
    if 'foto1' in request.FILES:
        if siswa.foto1 and os.path.exists(os.path.join(settings.MEDIA_ROOT, siswa.foto1.name)):
            os.remove(os.path.join(settings.MEDIA_ROOT, siswa.foto1.name))
        siswa.foto1 = request.FILES['foto1']

    if 'foto2' in request.FILES:
        if siswa.foto2 and os.path.exists(os.path.join(settings.MEDIA_ROOT, siswa.foto2.name)):
            os.remove(os.path.join(settings.MEDIA_ROOT, siswa.foto2.name))
        siswa.foto2 = request.FILES['foto2']

    if 'foto3' in request.FILES:
        if siswa.foto3 and os.path.exists(os.path.join(settings.MEDIA_ROOT, siswa.foto3.name)):
            os.remove(os.path.join(settings.MEDIA_ROOT, siswa.foto3.name))
        siswa.foto3 = request.FILES['foto3']
    siswa.save()
    return redirect('/admintpa/siswa')

def hapus_siswa(request):
    siswa = User.objects.get(role = 'siswa', id = request.POST['id_siswa'])

    folder_name = siswa.username.lower() + ", " + siswa.nama.lower()
    folder_path = os.path.join(settings.MEDIA_ROOT, 'images', folder_name)

    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    
    siswa.delete()
    return redirect('/admintpa/siswa')


def guru(request):
    guru = User.objects.filter(role = 'guru')
    return render(request, 'guru_admintpa/index.html', {'guru': guru})

def tambah_guru(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        nama = request.POST['nama']
        tmpt_lahir = request.POST['tmpt_lahir']
        tgl_lahir = request.POST['tgl_lahir']
        jkl = request.POST['jkl']
        agama = request.POST['agama']
        alamat = request.POST['alamat']
        notelp = request.POST['notelp']
        foto1 = request.FILES['foto1']
        foto2 = request.FILES['foto2']
        foto3 = request.FILES['foto3']

        user = User.objects.filter(username = username).first()
        if user :
            messages.error(request, "Username telah ada", extra_tags="duplicateUsername")
            return redirect('/admintpa/guru/tambah/')
        
        User.objects.create(
            username=username, 
            password=make_password(password),
            nama=nama,
            tmpt_lahir=tmpt_lahir,
            tgl_lahir=tgl_lahir,
            jkl=jkl,
            agama=agama,
            alamat=alamat,
            notelp=notelp,
            foto1=foto1,
            foto2=foto3,
            foto3=foto2,
            role="guru",
        )
        
        return redirect('/admintpa/guru')
    else:
        return render(request, 'guru_admintpa/tambah.html')

def edit_guru(request):
    guru = User.objects.get(role = 'guru', id = request.POST['id_guru'])
    return render(request, 'guru_admintpa/edit.html', {'guru': guru})

def proses_edit_guru(request):
    guru = User.objects.get(role = 'guru', id = request.POST['id_guru'])
    guru.username = request.POST['username']
    password = request.POST.get('password', None)
    if password:  # Hanya hash password jika ada input baru
        siswa.password = make_password(password)
    guru.nama = request.POST['nama']
    guru.tmpt_lahir = request.POST['tmpt_lahir']
    guru.tgl_lahir = request.POST['tgl_lahir']
    guru.jkl = request.POST['jkl']
    guru.agama = request.POST['agama']
    guru.alamat = request.POST['alamat']
    guru.notelp = request.POST['notelp']
    if 'foto1' in request.FILES:
        if guru.foto1 and os.path.exists(os.path.join(settings.MEDIA_ROOT, guru.foto1.name)):
            os.remove(os.path.join(settings.MEDIA_ROOT, guru.foto1.name))
        guru.foto1 = request.FILES['foto1']

    if 'foto2' in request.FILES:
        if guru.foto2 and os.path.exists(os.path.join(settings.MEDIA_ROOT, guru.foto2.name)):
            os.remove(os.path.join(settings.MEDIA_ROOT, guru.foto2.name))
        guru.foto2 = request.FILES['foto2']

    if 'foto3' in request.FILES:
        if guru.foto3 and os.path.exists(os.path.join(settings.MEDIA_ROOT, guru.foto3.name)):
            os.remove(os.path.join(settings.MEDIA_ROOT, guru.foto3.name))
        guru.foto3 = request.FILES['foto3']
    guru.save()
    return redirect('/admintpa/guru')

def hapus_guru(request):
    guru = User.objects.get(role = 'guru', id = request.POST['id_guru'])

    folder_name = guru.username.lower() + ", " + guru.nama.lower()
    folder_path = os.path.join(settings.MEDIA_ROOT, 'images', folder_name)

    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    guru.delete()
    return redirect('/admintpa/guru')

def kelas(request):
    query = """SELECT admintpa_kelas.id, admintpa_kelas.nama, admintpa_kelas.des, admintpa_user.nama AS guru
        FROM admintpa_kelas
        INNER JOIN admintpa_user ON admintpa_kelas.id_user = admintpa_user.id
        WHERE admintpa_user.role = 'guru'"""
    kelas = Kelas.objects.raw(query)
    return render(request, 'kelas_admintpa/index.html', {'kelas': kelas})

def tambah_kelas(request):
    guru = User.objects.filter(role = 'guru')
    if request.method == 'POST':
        id_guru = request.POST['id_guru']
        nama = request.POST['nama']
        deskripsi = request.POST['deskripsi']
        
        Kelas.objects.create(
            id_user = id_guru,
            nama=nama ,
            des=deskripsi,
        )
        
        return redirect('/admintpa/kelas')
    else:
        return render(request, 'kelas_admintpa/tambah.html', {'guru': guru})
    
def detail_kelas(request):
    kelas = Kelas.objects.get(id = request.GET['id_kelas'])

    query = """select admintpa_agtkelas.id as id, admintpa_user.nama, admintpa_user.tmpt_lahir, admintpa_user.tgl_lahir, 
    admintpa_user.jkl, admintpa_user.agama, admintpa_user.alamat, admintpa_user.notelp, 
    admintpa_user.foto1 as foto FROM admintpa_agtkelas 
    INNER JOIN admintpa_user on admintpa_agtkelas.id_user = admintpa_user.id WHERE admintpa_agtkelas.id_kelas = %s"""

    agtkelas = Agtkelas.objects.raw(query, [kelas.id])
    return render(request, 'kelas_admintpa/detail.html', {'agtkelas': agtkelas, 'kelas': kelas})

def tambah_agtkelas(request):
    kelas = Kelas.objects.get(id = request.POST['id_kelas'])
    query = """
        SELECT * 
        FROM admintpa_user 
        WHERE id NOT IN (SELECT id_user FROM admintpa_agtkelas) and role = 'siswa'
    """
    siswa = User.objects.raw(query)
    return render(request, 'kelas_admintpa/tambah-agt.html', {'siswa': siswa, 'kelas': kelas})
    

def proses_tambah_agtkelas(request):
    if request.method == 'POST':
        Agtkelas.objects.create(
            id_kelas = request.POST['id_kelas'],
            id_user = request.POST['id_siswa']
        )
        return redirect('/admintpa/kelas')


def hapus_agtkelas(request):
    agtkelas = Agtkelas.objects.get(id = request.POST['id_agtkelas'])
    agtkelas.delete()
    return redirect('/admintpa/kelas')

def edit_kelas(request):
    guru = User.objects.filter(role = 'guru')

    query = """SELECT admintpa_kelas.id, admintpa_kelas.nama, admintpa_kelas.des, admintpa_user.nama AS guru, admintpa_user.id as id_guru
        FROM admintpa_kelas
        INNER JOIN admintpa_user ON admintpa_kelas.id_user = admintpa_user.id
        WHERE admintpa_kelas.id = """+request.POST['id_kelas']
    kelas_list = list(Kelas.objects.raw(query))
    if kelas_list:
        kelas = kelas_list[0]
    else:
        kelas = None

    return render(request, 'kelas_admintpa/edit.html', {'kelas': kelas, 'guru': guru})

def proses_edit_kelas(request):
    kelas = Kelas.objects.get(id = request.POST['id_kelas'])
    kelas.nama = request.POST['nama']
    kelas.des = request.POST['deskripsi']
    kelas.id_user = request.POST['id_guru']
    kelas.save()
    return redirect('/admintpa/kelas')

def hapus_kelas(request):
    kelas = Kelas.objects.get(id = request.POST['id_kelas'])
    kelas.delete()
    return redirect('/admintpa/kelas')

def mapel(request):
    mapel = Mapel.objects.all()
    return render(request, 'mapel_admintpa/index.html',{'mapel': mapel})

def tambah_mapel(request):
    if request.method == 'POST':
        nama = request.POST['nama']
        deskripsi = request.POST['deskripsi']
        
        Mapel.objects.create(
            nama=nama, 
            des=deskripsi,
        )
        
        return redirect('/admintpa/mapel')
    else:
        return render(request, 'mapel_admintpa/tambah.html')

def edit_mapel(request):
    mapel = Mapel.objects.get(id=request.POST['id_mapel'])
    return render(request, 'mapel_admintpa/edit.html', {'mapel': mapel})

def proses_edit_mapel(request):
    mapel = Mapel.objects.get(id=request.POST['id_mapel'])
    mapel.nama = request.POST['nama']
    mapel.des = request.POST['deskripsi']
    mapel.save()
    return redirect('/admintpa/mapel')

def hapus_mapel(request):
    mapel = Mapel.objects.get(id=request.POST['id_mapel'])
    mapel.delete()
    return redirect('/admintpa/mapel')

def laporan(request):
    query = """SELECT admintpa_kelas.id, admintpa_kelas.nama, admintpa_kelas.des, admintpa_user.nama AS guru
        FROM admintpa_kelas
        INNER JOIN admintpa_user ON admintpa_kelas.id_user = admintpa_user.id
        WHERE admintpa_user.role = 'guru'"""
    kelas = Kelas.objects.raw(query)

    return render(request, 'laporan_admintpa/index.html', {'kelas': kelas})

def laporan_kelas(request):
    id_kelas = request.POST.get('id_kelas')
    
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
    WHERE admintpa_kelas.id = %s
    """
    
    kehadiran = Kehadiran.objects.raw(query, [id_kelas])
    kelas = Kelas.objects.get(id=id_kelas)

    return render(request, 'laporan_admintpa/detail.html', {'kehadiran': kehadiran, 'kelas': kelas})

def cetak_laporan(request):
    if request.method == "POST":
        id_kelas = request.POST.get('id_kelas')
        waktu = request.POST.get('waktu')
        
        # Query database (sama seperti sebelumnya)
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
        WHERE admintpa_kelas.id = %s
        """
        
        # Filter waktu (sama seperti sebelumnya)
        today = datetime.date.today()
        if waktu == "harian":
            query += " AND admintpa_absensi.tanggal = %s"
            params = [id_kelas, today]
        elif waktu == "mingguan":
            start_week = today - datetime.timedelta(days=today.weekday())
            query += " AND admintpa_absensi.tanggal BETWEEN %s AND %s"
            params = [id_kelas, start_week, today]
        elif waktu == "bulanan":
            start_month = today.replace(day=1)
            query += " AND admintpa_absensi.tanggal BETWEEN %s AND %s"
            params = [id_kelas, start_month, today]
        elif waktu == "tahunan":
            start_year = today.replace(month=1, day=1)
            query += " AND admintpa_absensi.tanggal BETWEEN %s AND %s"
            params = [id_kelas, start_year, today]
        else:
            params = [id_kelas]
            
        kehadiran = Kehadiran.objects.raw(query, params)
        kelas = Kelas.objects.get(id=id_kelas)
        
        # Render template HTML
        template = get_template('laporan_admintpa/laporan_pdf.html')
        html = template.render({'kehadiran': kehadiran, 'kelas': kelas})
        
        # Buat file PDF
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        
        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="laporan_absensi.pdf"'
            return response
        else:
            return HttpResponse("Error generating PDF", status=400)

# def laporan_kelas(request):

#     query = """SELECT admintpa_kehadiran.id AS id, admintpa_absensi.tanggal AS tanggal_absensi, 
#     admintpa_kelas.nama AS nama_kelas, admintpa_mapel.nama AS nama_mapel, 
#     admintpa_user.nama AS nama_user, admintpa_kehadiran.keterangan AS keterangan_kehadiran FROM admintpa_absensi 
#     INNER JOIN admintpa_kelas ON admintpa_absensi.id_kelas = admintpa_kelas.id 
#     INNER JOIN admintpa_mapel ON admintpa_absensi.id_mapel = admintpa_mapel.id 
#     INNER JOIN admintpa_kehadiran ON admintpa_absensi.id = admintpa_kehadiran.id_absensi 
#     INNER JOIN admintpa_agtkelas ON admintpa_kehadiran.id_agtkelas = admintpa_agtkelas.id 
#     INNER JOIN admintpa_user ON admintpa_agtkelas.id_user = admintpa_user.id where admintpa_absensi.id_kelas = %s"""
    
#     kehadiran = Kehadiran.objects.raw(query, [request.POST['id_kelas']])
#     return render(request, 'laporan_admintpa/detail.html', {'kehadiran': kehadiran, 'kelas': kelas})