from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from accounts.models import User, cnic_validator
from banking.models import Account


def admin_only(view):
    @wraps(view)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'admin':
            return redirect('user_dashboard')
        return view(request, *args, **kwargs)
    return wrapper


@admin_only
def admin_dashboard(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        cnic = request.POST.get('cnic', '').strip()
        password = request.POST.get('password', '')
        error = None
        try:
            cnic_validator(cnic)
        except ValidationError:
            error = 'CNIC must be exactly 13 digits (no dashes).'
        if not error and not name:
            error = 'Name is required.'
        if not error and len(password) < 6:
            error = 'Temporary password must be at least 6 characters.'
        if not error and User.objects.filter(cnic=cnic).exists():
            error = 'A user with this CNIC already exists.'

        if error:
            messages.error(request, error)
        else:
            with transaction.atomic():
                user = User.objects.create_user(
                    cnic=cnic, password=password, name=name,
                    role='user', created_by=request.user)
                account = Account.objects.create(user=user)
            messages.success(request, f'Account created for {name}. Account no: {account.account_number}')
        return redirect('admin_dashboard')

    context = {
        'users': User.objects.filter(created_by=request.user)
                     .select_related('account').order_by('-date_joined'),
        'total_users': User.objects.filter(role='user').count(),
        'active_users': User.objects.filter(role='user', is_active=True).count(),
        'total_admins': User.objects.filter(role='admin').count(),
    }
    return render(request, 'admin_dashboard.html', context)


@admin_only
@require_POST
def promote_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user.role == 'admin':
        messages.error(request, 'This user is already an admin.')
    else:
        user.role = 'admin'
        user.save()
        messages.success(request, f'{user.name or user.cnic} is now an admin.')
    return redirect('admin_dashboard')


@admin_only
@require_POST
def toggle_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.error(request, 'You cannot deactivate your own account.')
    else:
        user.is_active = not user.is_active
        user.save()
        state = 'activated' if user.is_active else 'deactivated'
        messages.success(request, f'{user.name or user.cnic} has been {state}.')
    return redirect('admin_dashboard')
