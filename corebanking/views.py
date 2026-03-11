from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import BankAccount
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

class DepositView(View):
    def get(self,request,*args,**kwargs):
        pk=kwargs.get("pk")
        account=BankAccount.objects.get(id=pk)
        return render(request,"deposit.html",{"account":account})
    
    def post(self,request,*args,**kwargs):
        pk=kwargs.get("pk")
        amount=float(request.POST.get("amount"))
        account=BankAccount.objects.get(id=pk)
        balance=account.deposit(amount)
        return render(request,'deposit.html',{"message":"Deposit successfully","balance":balance})
    
class WithdrawView(View):

    def get(self,request,*args,**kwargs):
        pk=kwargs.get("pk")
        account=BankAccount.objects.get(id=pk)
        balance=account.get_balance()
        return render(request,'withdraw.html',{'account':account,"balance":balance})
    def post(self,request,*args,**kwargs):
        pk=kwargs.get("pk")
        account=BankAccount.objects.get(id=pk)
        amount=float(request.POST.get("amount"))
        balance=account.withdraw(amount)
        return render(request,'withdraw.html',{"account":account,"amount":amount,"message":"Withdrawn successfully","balance":balance})

    
class AccountBalanceView(View):

    def get(self, request, *args,**kwargs):
        pk=kwargs.get("pk")
        account = BankAccount.objects.get(id=pk)
        balance = account.get_balance()
        return render(request,"balance.html",{"account": account, "balance": balance})