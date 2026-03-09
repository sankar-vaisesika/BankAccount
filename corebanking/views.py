from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import BankAccount
from django.http import JsonResponse
class DepositView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        amount=float(request.POST.get("amount"))
        account=BankAccount.objects.get(id=id)
        balance=account.deposit()
        return JsonResponse({"message":"Deposit successfully","balance":balance})
    
class AccountBalanceView(View):

    def get(self, request, *args,**kwargs):
        pk=kwargs.get(id=id)
        account = BankAccount.objects.get(id=pk)
        balance = account.get_balance()
        return render(request,"balance.html",{"account": account, "balance": balance})