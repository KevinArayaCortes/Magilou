from django.shortcuts import render, redirect
from AppMagilou.forms import RegistroForm
from AppMagilou.models import Producto
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from AppMagilou.models import Usuario



def car(request):
    return render(request, 'pago.html')

def catalogo(request):
    producto = Producto.objects.all()
    data = {'producto': producto }
    return render(request, 'catalogo.html', data)

def home(request):
    form = RegistroForm()  # Formulario de registro por defecto

    if request.method == 'POST':
        action = request.POST.get('action')  # Determina si es registro o login

        if action == 'register':
            # Procesar registro
            form = RegistroForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
                return redirect('/')  # Redirige tras registro exitoso
            else:
                messages.error(request, 'Hubo errores en el formulario de registro. Por favor, corrige y envía nuevamente.')

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
                    return redirect('/')  # Redirige tras inicio de sesión exitoso
                else:
                    messages.error(request, 'Contraseña incorrecta.')
            except Usuario.DoesNotExist:
                messages.error(request, 'El correo no está registrado.')

    # Renderiza la página principal con el formulario
    return render(request, 'home.html', {'form': form})
