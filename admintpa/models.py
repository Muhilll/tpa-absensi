from django.db import models
import os
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now

def upload_to(instance, filename):
    folder_name = instance.username.lower()+", "+instance.nama.lower()
    return os.path.join('images', folder_name, filename)

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    nama = models.CharField(max_length=100)
    tmpt_lahir = models.CharField(max_length=20)
    tgl_lahir = models.DateField()
    jkl = models.CharField(max_length=20)
    agama = models.CharField(max_length=20)
    alamat = models.CharField(max_length=50)
    notelp = models.CharField(max_length=20)
    foto1 = models.ImageField(upload_to=upload_to, blank=False, null=False)
    foto2 = models.ImageField(upload_to=upload_to, blank=False, null=False)
    foto3 = models.ImageField(upload_to=upload_to, blank=False, null=False)
    role = models.CharField(max_length=20)

class Kelas(models.Model):
    id_user = models.IntegerField()
    nama = models.CharField(max_length=100)
    des = models.CharField(max_length=100)

class Agtkelas(models.Model):
    id_kelas = models.IntegerField()
    id_user = models.IntegerField()

class Mapel(models.Model):
    nama = models.CharField(max_length=100)
    des = models.CharField(max_length=100)
    
class Absensi(models.Model):
    id_kelas = models.IntegerField()
    id_mapel = models.IntegerField()
    nama = models.CharField(max_length=100)
    tanggal = models.DateField()
    mulai = models.TimeField(default=now)
    batas = models.TimeField(default="00:00:00")
    des = models.CharField(max_length=255)

class Kehadiran(models.Model):
    id_absensi = models.IntegerField()
    id_agtkelas = models.IntegerField()
    tanggal = models.DateField(now)
    jam  = models.TimeField(default=now)
    keterangan = models.CharField(max_length=20)
