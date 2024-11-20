from django.shortcuts import render, redirect
from AppMagilou.forms import RegistroForm
from AppMagilou.models import Producto



def car(request):
    return render(request, 'pago.html')

def catalogo(request):
    producto = Producto.objects.all()
    data = {'producto': producto }
    return render(request, 'catalogo.html', data)

def home(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RegistroForm()

    return render(request, 'home.html', {'form': form})
 