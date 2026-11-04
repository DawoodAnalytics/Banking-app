from django.test import TestCase
from accounts.models import User
from accounts.validators import strength_error


class LoginTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            cnic='1111111111111', password='AdminPass123', role='admin')
        self.user = User.objects.create_user(
            cnic='2222222222222', password='UserPass123', role='user')

    def test_home_page_loads(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'User Login')
        self.assertContains(r, 'Admin Login')

    def test_user_login_success(self):
        r = self.client.post('/login/user/', {'cnic': '2222222222222', 'password': 'UserPass123'})
        self.assertRedirects(r, '/dashboard/', fetch_redirect_response=False)

    def test_admin_login_success(self):
        r = self.client.post('/login/admin/', {'cnic': '1111111111111', 'password': 'AdminPass123'})
        self.assertRedirects(r, '/manage/', fetch_redirect_response=False)

    def test_admin_cannot_use_user_login(self):
        r = self.client.post('/login/user/', {'cnic': '1111111111111', 'password': 'AdminPass123'})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'not a user account')

    def test_user_cannot_use_admin_login(self):
        r = self.client.post('/login/admin/', {'cnic': '2222222222222', 'password': 'UserPass123'})
        self.assertContains(r, 'not a admin account')

    def test_wrong_password_rejected(self):
        r = self.client.post('/login/user/', {'cnic': '2222222222222', 'password': 'wrong'})
        self.assertContains(r, 'Invalid CNIC or password')

    def test_deactivated_user_rejected(self):
        self.user.is_active = False
        self.user.save()
        r = self.client.post('/login/user/', {'cnic': '2222222222222', 'password': 'UserPass123'})
        self.assertContains(r, 'Invalid CNIC or password')

    def test_dashboard_requires_login(self):
        r = self.client.get('/dashboard/')
        self.assertEqual(r.status_code, 302)

    def test_user_cannot_open_admin_dashboard(self):
        self.client.login(username='2222222222222', password='UserPass123')
        r = self.client.get('/manage/')
        self.assertRedirects(r, '/dashboard/', fetch_redirect_response=False)

    def test_logout(self):
        self.client.login(username='2222222222222', password='UserPass123')
        self.client.get('/logout/')
        r = self.client.get('/dashboard/')
        self.assertEqual(r.status_code, 302)


class PasswordStrengthTests(TestCase):
    def test_valid_password_passes(self):
        self.assertIsNone(strength_error('Ali@Secure2026'))

    def test_too_short(self):
        self.assertIsNotNone(strength_error('Ab1@xyz'))

    def test_no_uppercase(self):
        self.assertIsNotNone(strength_error('ali@secure2026'))

    def test_no_lowercase(self):
        self.assertIsNotNone(strength_error('ALI@SECURE2026'))

    def test_no_number(self):
        self.assertIsNotNone(strength_error('Ali@SecurePass'))

    def test_no_symbol(self):
        self.assertIsNotNone(strength_error('AliSecure20261'))

    def test_admin_cannot_create_user_with_weak_password(self):
        User.objects.create_user(cnic='1111111111111', password='Admin@Pass2026', role='admin')
        self.client.login(username='1111111111111', password='Admin@Pass2026')
        self.client.post('/manage/', {'name': 'Ali', 'cnic': '4210112345672', 'password': 'temp1234'})
        self.assertFalse(User.objects.filter(cnic='4210112345672').exists())

    def test_admin_can_create_user_with_strong_password(self):
        User.objects.create_user(cnic='1111111111111', password='Admin@Pass2026', role='admin')
        self.client.login(username='1111111111111', password='Admin@Pass2026')
        self.client.post('/manage/', {'name': 'Ali', 'cnic': '4210112345672', 'password': 'Ali@Secure2026'})
        self.assertTrue(User.objects.filter(cnic='4210112345672').exists())
