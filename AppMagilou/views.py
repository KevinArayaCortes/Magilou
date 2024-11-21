from django.shortcuts import render, redirect
from AppMagilou.forms import RegistroForm
from AppMagilou.models import Producto
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from AppMagilou.models import Usuario, CarroDeCompras, CarroProducto
from django.http import JsonResponse
from django.shortcuts import get_object_or_404



def car(request):
    return render(request, 'pago.html')

def catalogo(request):
    producto = Producto.objects.all()
    data = {'producto': producto }
    return render(request, 'catalogo.html', data)

def home(request):
    form = RegistroForm()  # Formulario de registro por defecto

    if request.method == 'POST':
        action = request.POST.get('action')  # Determina si es login, registro o logout

        if action == 'register':
            # Procesar registro
            form = RegistroForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
                return redirect('/')
            else:
                messages.error(request, 'Hubo errores en el formulario. Corrige y envía nuevamente.')

        elif action == 'login':
            # Procesar inicio de sesión
            correo = request.POST.get('correo')
            contrasena = request.POST.get('contrasena')

            try:
                usuario = Usuario.objects.get(correo=correo)
                if check_password(contrasena, usuario.contrasena):
                    # Guardar datos en la sesión
                    request.session['usuario_id'] = usuario.id_usuario
                    request.session['usuario_nombre'] = usuario.nombre
                    messages.success(request, f'Bienvenido, {usuario.nombre}!')
                    return redirect('/')
                else:
                    messages.error(request, 'Contraseña incorrecta.')
            except Usuario.DoesNotExist:
                messages.error(request, 'El correo no está registrado.')

        elif action == 'logout':
            # Procesar cierre de sesión
            if 'usuario_id' in request.session:
                del request.session['usuario_id']
                del request.session['usuario_nombre']
                messages.success(request, 'Has cerrado sesión correctamente.')
            return redirect('/')

    return render(request, 'home.html', {'form': form})

