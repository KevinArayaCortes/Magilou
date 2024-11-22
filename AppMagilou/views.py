from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from AppMagilou.forms import RegistroForm
from AppMagilou.models import Usuario, Producto, CarroDeCompras, CarroProducto
import json


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

# Vista de catálogo
def catalogo(request):
    query = request.GET.get('q', '')  # Término de búsqueda
    tipo_filtro = request.GET.get('tipo', '')  # Filtro por tipo
    
    # Obtener todos los tipos de productos para el filtro
    tipos = Producto.objects.values_list('tipo_producto', flat=True).distinct()
    
    # Filtrar productos según búsqueda y tipo
    producto = Producto.objects.all()
    if query:
        producto = producto.filter(
            nombre_producto__icontains=query
        ) | producto.filter(
            descripcion_producto__icontains=query
        )
    if tipo_filtro:
        producto = producto.filter(tipo_producto=tipo_filtro)

    data = {
        'producto': producto,
        'tipos': tipos,
        'query': query,
        'tipo_filtro': tipo_filtro,
    }
    return render(request, 'catalogo.html', data)

# Vista del carrito de compras
def car(request):
    return render(request, 'pago.html')

# Agregar producto al carrito
@csrf_exempt
def agregar_carrito(request):
    if request.method == "POST":
        # Obtener el ID del usuario desde la sesión
        usuario_id = request.session.get('usuario_id')  # Asegúrate de que exista esta sesión en tu app
        if not usuario_id:
            return JsonResponse({"error": "Usuario no autenticado"}, status=401)

        # Parsear los datos enviados
        data = json.loads(request.body)
        producto_id = data.get("producto_id")

        # Validar si el producto existe
        try:
            producto = Producto.objects.get(id_producto=producto_id)
        except Producto.DoesNotExist:
            return JsonResponse({"error": "Producto no encontrado"}, status=404)

        # Obtener o crear el carrito asociado al usuario
        carrito, creado = CarroDeCompras.objects.get_or_create(
            id_usuario_id=usuario_id, estado="pendiente",
            defaults={"fecha": date.today(), "cantidad_productos": 0, "precio_total": 0.0}
        )

        # Verificar si el producto ya está en el carrito
        carro_producto, creado = CarroProducto.objects.get_or_create(
            id_carro=carrito, id_producto=producto,
            defaults={"cantidad_producto": 1}
        )
        if not creado:
            carro_producto.cantidad_producto += 1
            carro_producto.save()

        # Actualizar el carrito
        carrito.cantidad_productos += 1
        carrito.precio_total += producto.precio_producto
        carrito.save()

        # Preparar datos del carrito para la respuesta
        carrito_productos = CarroProducto.objects.filter(id_carro=carrito).select_related("id_producto")
        productos = [
            {
                "nombre": cp.id_producto.nombre_producto,
                "precio": cp.id_producto.precio_producto,
                "cantidad": cp.cantidad_producto
            }
            for cp in carrito_productos
        ]

        return JsonResponse({"carrito": productos, "total": carrito.precio_total})
    return JsonResponse({"error": "Método no permitido"}, status=405)

# Mostrar productos en el carrito
def mostrar_carrito(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return render(request, "carrito.html", {"error": "No hay usuario autenticado."})

    try:
        carrito = CarroDeCompras.objects.get(id_usuario_id=usuario_id, estado="pendiente")
        carrito_productos = CarroProducto.objects.filter(id_carro=carrito).select_related("id_producto")
    except CarroDeCompras.DoesNotExist:
        carrito_productos = []
        carrito = None

    return render(request, "carrito.html", {
        "carrito": carrito,
        "productos": carrito_productos,
    })

@csrf_exempt
def eliminar_carrito(request):
    if request.method == "POST":
        # Obtener el ID del usuario desde la sesión
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            return JsonResponse({"error": "Usuario no autenticado"}, status=401)

        # Parsear los datos enviados
        data = json.loads(request.body)
        producto_id = data.get("producto_id")

        # Validar si el producto existe en el carrito del usuario
        try:
            carrito = CarroDeCompras.objects.get(id_usuario_id=usuario_id, estado="pendiente")
            carro_producto = CarroProducto.objects.get(id_carro=carrito, id_producto_id=producto_id)
        except (CarroDeCompras.DoesNotExist, CarroProducto.DoesNotExist):
            return JsonResponse({"error": "Producto no encontrado en el carrito"}, status=404)

        # Restar cantidad o eliminar producto
        if carro_producto.cantidad_producto > 1:
            carro_producto.cantidad_producto -= 1
            carro_producto.save()
        else:
            carro_producto.delete()

        # Actualizar el carrito
        carrito.cantidad_productos -= 1
        carrito.precio_total -= carro_producto.id_producto.precio_producto
        carrito.save()

        # Preparar datos del carrito para la respuesta
        carrito_productos = CarroProducto.objects.filter(id_carro=carrito).select_related("id_producto")
        productos = [
            {
                "nombre": cp.id_producto.nombre_producto,
                "precio": cp.id_producto.precio_producto,
                "cantidad": cp.cantidad_producto
            }
            for cp in carrito_productos
        ]

        return JsonResponse({"carrito": productos, "total": carrito.precio_total})
    return JsonResponse({"error": "Método no permitido"}, status=405)
