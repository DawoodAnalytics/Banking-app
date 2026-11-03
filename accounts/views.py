from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def _dashboard_for(user):
    return 'admin_dashboard' if user.role == 'admin' else 'user_dashboard'


def home(request):
    if request.user.is_authenticated:
        return redirect(_dashboard_for(request.user))
    return render(request, 'home.html')


def role_login(request, role):
    if request.user.is_authenticated:
        return redirect(_dashboard_for(request.user))
    if request.method == 'POST':
        cnic = request.POST.get('cnic', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=cnic, password=password)
        if user is None:
            messages.error(request, 'Invalid CNIC or password, or account is deactivated.')
        elif user.role != role:
            messages.error(request, f'This is not a {role} account.')
        else:
            login(request, user)
            return redirect(_dashboard_for(user))
    return render(request, 'login.html', {'role': role})


def user_login(request):
    return role_login(request, 'user')


def admin_login(request):
    return role_login(request, 'admin')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def user_dashboard(request):
    if request.user.role != 'user':
        return redirect('admin_dashboard')
    return render(request, 'dashboard.html', {'role': 'user'})


@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('user_dashboard')
    return render(request, 'dashboard.html', {'role': 'admin'})
