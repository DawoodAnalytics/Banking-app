from decimal import Decimal
from django.test import TestCase
from accounts.models import User
from banking.models import Account


class AccountTests(TestCase):
    def test_account_number_is_10_digits(self):
        u = User.objects.create_user(cnic='3333333333333', password='Pass12345')
        a = Account.objects.create(user=u)
        self.assertEqual(len(a.account_number), 10)
        self.assertTrue(a.account_number.isdigit())

    def test_account_numbers_are_unique(self):
        u1 = User.objects.create_user(cnic='4444444444444', password='Pass12345')
        u2 = User.objects.create_user(cnic='5555555555555', password='Pass12345')
        a1 = Account.objects.create(user=u1)
        a2 = Account.objects.create(user=u2)
        self.assertNotEqual(a1.account_number, a2.account_number)

    def test_new_account_defaults(self):
        u = User.objects.create_user(cnic='6666666666666', password='Pass12345')
        a = Account.objects.create(user=u)
        self.assertEqual(a.balance, Decimal('0.00'))
        self.assertEqual(a.credit_score, 500)
