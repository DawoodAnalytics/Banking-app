from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models

cnic_validator = RegexValidator(r'^\d{13}$', 'CNIC must be exactly 13 digits (no dashes).')


class UserManager(BaseUserManager):
    def create_user(self, cnic, password=None, **extra):
        if not cnic:
            raise ValueError('CNIC is required')
        user = self.model(cnic=cnic, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cnic, password=None, **extra):
        extra.setdefault('role', 'admin')
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        return self.create_user(cnic, password, **extra)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [('user', 'User'), ('admin', 'Admin')]

    cnic = models.CharField(max_length=13, unique=True, validators=[cnic_validator])
    name = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_profile_complete = models.BooleanField(default=False)
    created_by = models.ForeignKey('self', null=True, blank=True,
                                   on_delete=models.SET_NULL, related_name='created_users')
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'cnic'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return f'{self.cnic} ({self.role})'
