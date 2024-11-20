from django.shortcuts import render, redirect
from AppMagilou.forms import RegistroForm
from AppMagilou.models import Producto
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from AppMagilou.models import Usuario

def inicio_sesion(request):
    if request.method == 'POST':
        correo = request.POST['correo']
        contrasena = request.POST['contrasena']

        try:
            usuario = Usuario.objects.get(correo=correo)

            # Verificar si la contraseña coincide
            if check_password(contrasena, usuario.contrasena):
                # Guardar datos en la sesión
                request.session['usuario_id'] = usuario.id_usuario
                request.session['usuario_nombre'] = usuario.nombre
                return redirect('/')
            else:
                messages.error(request, 'Contraseña incorrecta.')
        except Usuario.DoesNotExist:
            messages.error(request, 'El correo no está registrado.')

    return render(request, 'inicio_sesion.html')


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
 