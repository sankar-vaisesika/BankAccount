from django.db import models

# Create your models here.
from django.db.models import Sum,Count
import random
from django.contrib.auth.models import User

class BankAccount(models.Model):
    ACCOUNT_TYPES=(
        ("SAVINGS","saving"),
        ("CURRENT","current"),
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    account_number=models.CharField(max_length=10,unique=True,blank=True)
    account_type=models.CharField(max_length=10,choices=ACCOUNT_TYPES)
    created_at=models.DateTimeField(auto_now_add=True)
    balance=models.DecimalField(max_digits=12,decimal_places=2,default=0)

    def save(self,*args,**kwargs):
        if not self.account_number:
            self.account_number=str(random.randint(100000,999999))
        super().save(*args,**kwargs)    

    # def get_balance(self):
    #     deposits=self.transactions.filter(transaction_type="DEPOSIT").aggregate(total=Sum("amount"))["total"] or 0

    #     withdrawals=self.transactions.filter(transaction_type="WITHDRAW").aggregate(total=Sum("amount"))["total"] or 0

    #     return deposits-withdrawals
    
    def deposit(self,amount):

        if amount<=0:
            raise ValueError("Invalid amount")

        self.balance+=amount
        self.save()
        Transaction.objects.create(account=self,transaction_type="DEPOSIT",amount=amount)

        return self.balance
    
    def withdraw(self, amount):

        if amount <= 0:
            return "Invalid amount"

        if amount > self.balance:
            return "Insufficient balance"
        
        self.balance-=amount
        self.save()
        Transaction.objects.create(
            account=self,
            transaction_type="WITHDRAW",
            amount=amount
        )

        return self.balance

    def __str__(self):
        return f"{self.name}-{self.account_number}"
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
    

