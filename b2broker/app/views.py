from django.shortcuts import render

from app.models import Wallet, Transaction


def index(request):
    return 'hello'
