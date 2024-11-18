from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def car(request):
    return render(request, 'pago.html')
 