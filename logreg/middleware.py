from django.shortcuts import redirect
from django.contrib import messages
from django.urls import resolve
import re

class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List URL yang diizinkan untuk diakses tanpa login
        public_paths = [
            r'^/auth/',
            r'^/static/',
            r'^/media/',
        ]

        # Cek apakah URL saat ini adalah public path
        current_path = request.path
        if any(re.match(pattern, current_path) for pattern in public_paths):
            return self.get_response(request)

        # Cek session
        if not request.session.get('id_user'):
            messages.error(request, 'Silakan login terlebih dahulu.')
            return redirect('/auth/')

        try:
            # Import User model
            from admintpa.models import User
            user = User.objects.get(id=request.session['id_user'])

            # Mendapatkan path pertama dari URL (siswa, guru, atau admintpa)
            path = request.path.split('/')[1]

            # Cek akses berdasarkan role
            if user.role == 'siswa' and path != 'siswa':
                messages.error(request, 'Akses ditolak!')
                return redirect('/siswa/')
            elif user.role == 'guru' and path != 'guru':
                messages.error(request, 'Akses ditolak!')
                return redirect('/guru/')
            elif user.role == 'admin' and path != 'admintpa':
                messages.error(request, 'Akses ditolak!')
                return redirect('/admintpa/')

        except User.DoesNotExist:
            # Jika user tidak ditemukan, hapus session
            del request.session['id_user']
            messages.error(request, 'Sesi Anda telah berakhir.')
            return redirect('/auth/')

        # Lanjutkan ke view jika semua pengecekan berhasil
        response = self.get_response(request)
        return response