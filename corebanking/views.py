from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import BankAccount
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login,authenticate,logout
from corebanking.forms import RegisterForm,BankAccountForm
from django.shortcuts import redirect
from decimal import Decimal

class RegisterView(View):

    def get(self,request):

        user_form = RegisterForm()
        account_form = BankAccountForm()

        return render(request,"register.html",{
            "user_form":user_form,
            "account_form":account_form
        })


    def post(self,request):

        user_form = RegisterForm(request.POST)
        account_form = BankAccountForm(request.POST)

        if user_form.is_valid() and account_form.is_valid():

            user = user_form.save(commit=False)

            # password hashing
            user.set_password(user_form.cleaned_data["password"])
            user.save()

            account = account_form.save(commit=False)
            account.user = user
            account.save()

            login(request,user)

            return redirect("balance",pk=account.id)

        return render(request,"register.html",{
            "user_form":user_form,
            "account_form":account_form
        })
    
class LoginView(View):

    def get(self,request):
        return render(request,"login.html")


    def post(self,request):

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request,user)

            account = BankAccount.objects.get(user=user)

            return redirect("balance",pk=account.id)

        return render(request,"login.html",{
            "error":"Invalid credentials"
        })
    
class LogoutView(View):

    def get(self,request):

        logout(request)

        return redirect("login")
    
class DepositView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        pk=kwargs.get("pk")
        account=get_object_or_404(BankAccount,id=pk,user=request.user)
        return render(request,"deposit.html",{"account":account})
    
    def post(self,request,*args,**kwargs):
        pk=kwargs.get("pk")
        account=get_object_or_404(BankAccount,id=pk,user=request.user)
        try:
            amount=Decimal(request.POST.get("amount"))
            balance=account.deposit(amount)
            message="Deposit successfully"
        except ValueError as e:
            balance=account.balance
            message=str(e)

        return render(request,'deposit.html',{"account":account,
                                              "message":message,
                                              "balance":balance})
    
class WithdrawView(View):

    def get(self,request,*args,**kwargs):
        pk=kwargs.get("pk")
        account=get_object_or_404(BankAccount,id=pk,user=request.user)
        return render(request,'withdraw.html',{'account':account,"balance":account.balance})
    def post(self,request,*args,**kwargs):
        pk=kwargs.get("pk")
        account=get_object_or_404(BankAccount,id=pk,user=request.user)
        try:
            amount=Decimal(request.POST.get("amount"))
            balance=account.withdraw(amount)
            message="Withdrawn successfully"
        except ValueError as e:
            balance=account.balance
            message=str(e)

        return render(request,'withdraw.html',{"account":account,
                                               "amount":amount,
                                               "message":message,
                                               "balance":balance})

    
class AccountBalanceView(LoginRequiredMixin,View):

    def get(self, request, *args,**kwargs):
        pk=kwargs.get("pk")
        account = get_object_or_404(BankAccount,id=pk,user=request.user)
        return render(request,"balance.html",{"account": account, "balance": account.balance})