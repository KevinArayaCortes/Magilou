from django.shortcuts import render, redirect
from AppMagilou.forms import RegistroForm

def home(request):
    return render(request, 'home.html')

def car(request):
    return render(request, 'pago.html')

def catalogo(request):
    return render(request, 'catalogo.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})
 