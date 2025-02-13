from django.shortcuts import render, redirect
from django.contrib import messages
from admintpa.models import User
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password


def login(request):
    
    return render(request, 'login.html')


def proses_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']
        try:
            user = User.objects.get(username=username, role=role)
            if check_password(password, user.password):
                # Set session
                request.session['id_user'] = user.id
                
                # Redirect berdasarkan role
                if user.role == 'admin':
                    return redirect('/admintpa/')
                elif user.role == 'guru':
                    return redirect('/guru/')
                elif user.role == 'siswa':
                    return redirect('/siswa/')
            else:
                messages.error(request, 'Password salah.')
        except User.DoesNotExist:
            messages.error(request, 'Username tidak terdaftar.')
            
    return redirect('/auth/')

def logout(request):
    if 'id_user' in request.session:
        del request.session['id_user']
    messages.success(request, 'Berhasil logout.')
    return redirect('/auth/')