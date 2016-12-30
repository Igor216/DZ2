from django.shortcuts import render, get_object_or_404
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, logout
from django.views.generic import ListView

from polls.models import *
from polls.forms import SignupForm, SigninForm

from django.http import Http404
from .models import *


def home(request):
    banks = BankModel.objects.all()
    context = {
        'banks': banks
    }
    return render(request, "home.html", context)


def about(request):
    return render(request, 'about.html')


def show_bank(request, idbank):
    bank = get_object_or_404(BankModel, id=int(idbank))
    return render(request, "bank.html", {'bank': bank})






def main(request):
    users = User.objects.all()

    return render(request, 'main.html', {
        'users': users
    })


def signup(request):
    redirect = request.GET.get('continue', '/')
    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect)

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return HttpResponseRedirect(redirect)
    else:
        form = SignupForm()

    return render(request, 'signup.html', {
        'form': form
    })


def signin(request):
    redirect = request.GET.get('continue', '/success')
    if request.method == "POST":
        form = SigninForm(request.POST)

        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            return HttpResponseRedirect(redirect)
    else:
        form = SigninForm()
    return render(request, 'signin.html', {
        'form': form
    })


@login_required(redirect_field_name='continue')
def login_success(request):
    return render(request, 'success.html')


def logout(request):
    redirect = request.GET.get('continue', '/')
    auth.logout(request)
    return HttpResponseRedirect(redirect)


class UserView(View):
    def get(self, request, id):
        user = User.objects.get(id=int(id))

        transactions = TransactionModel.objects.filter(user=user).all()

        return render(request, 'user.html', {
            'user': user,
            'transactions': transactions
        })

class CreateTransactionForm(forms.ModelForm):


    def __init__(self, user, *args, **kwargs):
        super(CreateTransactionForm, self).__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = TransactionModel
        fields = ('idtran', 'sum', 'type', 'user', 'bank', 'image')

    def save(self, commit=False):
        instance = super(CreateTransactionForm, self).save(commit=True)
        instance.user = self.user

        return instance

@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = CreateTransactionForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            form.save(True)
            return redirect('home')
    else:
        form = CreateTransactionForm(request.user)

    return render(request, 'create_transaction.html', {'form': form})
