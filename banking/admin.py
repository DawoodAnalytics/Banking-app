from django.contrib import admin
from .models import Account, Transaction

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'user', 'balance', 'credit_score', 'created_at')
    search_fields = ('account_number', 'user__cnic')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'type', 'amount', 'to_account', 'balance_after', 'timestamp')
    list_filter = ('type',)
