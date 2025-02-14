from django.shortcuts import render, redirect
from admintpa.models import Agtkelas, User, Absensi, Kehadiran, Kelas
import cv2
import numpy as np
from django.contrib import messages
from django.conf import settings
import os
from django.utils.timezone import now
from django.utils.timezone import localtime

def index(request):
    id_user = request.session.get('id_user')
    agtkelas = Agtkelas.objects.get(id_user = id_user)
    query = """
        SELECT admintpa_kehadiran.id AS id,
                admintpa_absensi.tanggal AS tanggal_absensi, 
                admintpa_kehadiran.jam AS jam, 
                admintpa_kelas.nama AS nama_kelas, 
                admintpa_mapel.nama AS nama_mapel, 
                admintpa_user.nama AS nama_user, 
                admintpa_kehadiran.keterangan AS keterangan_kehadiran
            FROM admintpa_absensi
            INNER JOIN admintpa_kelas ON admintpa_absensi.id_kelas = admintpa_kelas.id
            INNER JOIN admintpa_mapel ON admintpa_absensi.id_mapel = admintpa_mapel.id
            INNER JOIN admintpa_kehadiran ON admintpa_absensi.id = admintpa_kehadiran.id_absensi
            INNER JOIN admintpa_agtkelas ON admintpa_kehadiran.id_agtkelas = admintpa_agtkelas.id
            INNER JOIN admintpa_user ON admintpa_agtkelas.id_user = admintpa_user.id where admintpa_kelas.id = %s AND admintpa_kehadiran.id_agtkelas = %s
            ORDER BY admintpa_absensi.tanggal DESC
            LIMIT 10
    """
    kehadiran = Kehadiran.objects.raw(query, [agtkelas.id_kelas, agtkelas.id])
    return render(request, 'home_siswa/index.html', {'kehadiran': kehadiran})

def absensi(request):
    id_user = request.session.get('id_user')
    agtkelas = Agtkelas.objects.get(id_user = id_user)

    absensi_list = Absensi.objects.filter(id_kelas=agtkelas.id_kelas)

    for absensi in absensi_list:
        if now().time() > absensi.batas:
            kehadiran, created = Kehadiran.objects.get_or_create(
                id_absensi=absensi.id,
                id_agtkelas=agtkelas.id,
                defaults={"keterangan": "apla", "tanggal": now()},
            )
            if not created and kehadiran.keterangan is None:
                kehadiran.keterangan = "apla"
                kehadiran.save()

    query = """SELECT admintpa_absensi.id AS id, admintpa_mapel.nama as mapel,
            admintpa_absensi.nama, 
            admintpa_absensi.tanggal, 
            admintpa_absensi.mulai, 
            admintpa_absensi.batas, 
            admintpa_absensi.des, 
            admintpa_kehadiran.keterangan 
        FROM admintpa_absensi
        INNER JOIN admintpa_mapel on admintpa_absensi.id_mapel = admintpa_mapel.id
        LEFT JOIN admintpa_kehadiran ON admintpa_absensi.id = admintpa_kehadiran.id_absensi 
        AND admintpa_kehadiran.id_agtkelas = %s
        WHERE admintpa_absensi.id_kelas = %s ORDER BY tanggal DESC
    """
    absensi = Absensi.objects.raw(query, [agtkelas.id, agtkelas.id_kelas])

    return render(request, 'absensi_siswa/index.html', {'absensi': absensi})

model = cv2.dnn.readNetFromONNX("siswa/yolov11n-face.onnx")

def submit(request):
    id_absensi = request.POST['id_absensi']
    absensi = Absensi.objects.get(id=id_absensi)
    id_user = request.session.get('id_user')
    agtkelas = Agtkelas.objects.get(id_user=id_user)
    return render(request, 'absensi_siswa/submit.html', {'absensi': absensi, 'id_agtkelas': agtkelas.id})

def proses_submit(request):
    if request.method == 'POST':
        id_absensi = request.POST.get('id_absensi')
        id_agtkelas = request.POST.get('id_agtkelas')
        keterangan = request.POST.get('keterangan')

        if keterangan != "hadir":
            Kehadiran.objects.create(
                id_absensi=id_absensi,
                id_agtkelas=id_agtkelas,
                keterangan=keterangan,
                tanggal=now().date(),
                jam=localtime().time(),
            )
            return redirect('/siswa/absensi/')

        # Load foto user dari database
        query = """SELECT admintpa_user.id as id, admintpa_user.nama, admintpa_user.foto1 FROM admintpa_user 
        INNER JOIN admintpa_agtkelas on admintpa_user.id = admintpa_agtkelas.id_user WHERE admintpa_agtkelas.id = %s"""
        agtkelas = Agtkelas.objects.raw(query, [id_agtkelas])

        if not agtkelas:
            return redirect('/siswa/absensi/')

        user_image_path = "media/" + agtkelas[0].foto1
        user_id = agtkelas[0].id
        user_name = agtkelas[0].nama

        # Load foto wajah pengguna
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        image = cv2.imread(user_image_path, cv2.IMREAD_GRAYSCALE)

        if image is None:
            return redirect('/siswa/absensi/')

        faces = []
        labels = []

        # Deteksi wajah di gambar
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        detected_faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in detected_faces:
            faces.append(image[y:y+h, x:x+w])
            labels.append(user_id)

        if len(faces) == 0:
            return redirect('/siswa/absensi/')

        # Training model dengan satu wajah pengguna
        face_recognizer.train(faces, np.array(labels))

        video_capture = cv2.VideoCapture(0)
        terdeteksi = False

        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detected_faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in detected_faces:
                face_roi = gray[y:y+h, x:x+w]

                # Prediksi wajah
                label, confidence = face_recognizer.predict(face_roi)

                if label == user_id and confidence < 50:  # Confidence threshold
                    terdeteksi = True
                    color = (0, 255, 0)
                    text = f"{user_name} ({confidence:.2f})"
                else:
                    color = (0, 0, 255)
                    text = "Unknown"

                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            cv2.imshow("Face Recognition OpenCV LBPH", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

        if terdeteksi:
            Kehadiran.objects.create(
                id_absensi=id_absensi,
                id_agtkelas=id_agtkelas,
                keterangan='hadir',
                tanggal=now().date(),
                jam=localtime().time(),
            )

        return redirect('/siswa/absensi/')

def profile(request):
    id_user = request.session.get('id_user')
    user = User.objects.get(id = id_user)

    return render(request, 'profile_siswa/index.html', {'user': user})

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
        return redirect('/siswa/profile')
    else:
        return render(request, 'profile_siswa/edit.html', {'user': user})
    

def logout(request):
    if request.method == 'POST':
        if 'id_user' in request.session:
            del request.session['id_user']
            messages.success(request, 'Anda berhasil logout.')
    return redirect('/auth/')