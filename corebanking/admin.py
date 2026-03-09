from django.contrib import admin
from corebanking.models import BankAccount,Transaction
# Register your models here.
admin.site.register(BankAccount)
admin.site.register(Transaction)
