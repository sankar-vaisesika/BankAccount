from django.db import models

# Create your models here.
from django.db.models import Sum,Count
import random

class BankAccount(models.Model):
    ACCOUNT_TYPES=(
        ("SAVINGS","saving"),
        ("CURRENT","current"),
    )

    name=models.CharField(max_length=100)
    account_number=models.CharField(max_length=10,unique=True)
    account_type=models.CharField(max_length=10,choices=ACCOUNT_TYPES)
    created_at=models.DateTimeField(auto_now_add=True)

    def save(self,*args,**kwargs):
        if not self.account_number:
            self.account_number=str(random.randint(100000,999999))
        super().save(*args,**kwargs)

    def get_balance(self):
        deposits=self.transactions.filter(transaction_type="DEPOSIT").aggregate(total=Sum("amount"))["total"] or 0

        withdrawals=self.transactions.filter(transaction_type="WITHDRAW").aggregate(total=Sum("amount"))["total"] or 0

        return deposits-withdrawals
     
    def __str__(self):
        return f"{self.name}-{self.account_number}"
    
    def deposit(self,amount):
        if amount<=0:
            raise ValueError("Invalid amount")
        Transaction.objects.create(account=self,transaction_type="DEPOSIT",amount=amount)

        return self.get_balance()
    
    def withdraw(self,amount):

        balance=self.get_balance()

        if self.account_type=="SAVINGS":

            if amount>balance:
                raise ValueError("Insufficient amount")

        elif self.account_type=="CURRENT":
            limit=1000

            if amount>limit+balance:
                raise ValueError("overdraft exceeded")

        Transaction.objects.create(account=self,transaction_type="WITHDRAW",amount=amount)

        return self.get_balance()
    
class Transaction(models.Model):
    
    TRANSACTION_TYPES=(
        ('DEPOSIT','deposit'),
        ('WITHDRAW','withdraw'),
    )

    account=models.ForeignKey(BankAccount,on_delete=models.CASCADE,related_name="transactions")
    transaction_type=models.CharField(max_length=10,choices=TRANSACTION_TYPES)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.transaction_type} -{self.amount}"
    

