from gettext import translation
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from datetime import date
from AppMagilou.forms import RegistroForm
from AppMagilou.models import Usuario, Producto, CarroDeCompras, CarroProducto
import json
from django.contrib.auth import logout as auth_logout
from datetime import datetime

from decimal import Decimal


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

    # Formatear los precios a formato sin símbolo de peso y con coma como separador de miles
    for prod in producto:
        prod.precio_formateado = f"{prod.precio_producto:,.0f}".replace(",", ".")
    
    data = {
        'producto': producto,
        'tipos': tipos,
        'query': query,
        'tipo_filtro': tipo_filtro,
    }
    return render(request, 'catalogo.html', data)



# Vista para mostrar el carrito
def mostrar_carrito(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return render(request, "home.html", {"error": "No hay usuario autenticado."})

    try:
        carrito = CarroDeCompras.objects.get(id_usuario_id=usuario_id, estado="pendiente")
        carrito_productos = CarroProducto.objects.filter(id_carro=carrito).select_related("id_producto")

        # Calcular el total del carrito
        total = sum(Decimal(producto.cantidad_producto) * Decimal(producto.id_producto.precio_producto) for producto in carrito_productos)
        
        # Formatear el total con el formato chileno (con puntos como separador de miles)
        total_formateado = f"${total:,.0f}".replace(",", ".")  # Formato chileno
    except CarroDeCompras.DoesNotExist:
        carrito_productos = []
        carrito = None
        total_formateado = "$0"  # Valor predeterminado si no se encuentra el carrito

    data = {
        "carrito": carrito,
        "productos": carrito_productos,
        "total": total_formateado,  # Pasar el total ya formateado
    }
    return render(request, "carrito.html", data)

def eliminar_producto_carrito(request, producto_id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "No hay usuario autenticado.")
        return redirect("mostrar_carrito")

    try:
        carrito = CarroDeCompras.objects.get(id_usuario_id=usuario_id, estado="pendiente")
        producto = get_object_or_404(CarroProducto, id_carro=carrito, id_producto=producto_id)
        producto.delete()
        messages.success(request, "Producto eliminado del carrito correctamente.")
    except CarroDeCompras.DoesNotExist:
        messages.error(request, "No se encontró un carrito pendiente.")
    except CarroProducto.DoesNotExist:
        messages.error(request, "El producto no está en el carrito.")

    return redirect("mostrar_carrito")


def actualizar_cantidad_producto(request, producto_id):
    if request.method == "POST":
        nueva_cantidad = request.POST.get("cantidad")
        try:
            usuario_id = request.session.get('usuario_id')
            carrito = CarroDeCompras.objects.get(id_usuario_id=usuario_id, estado="pendiente")
            producto = CarroProducto.objects.get(id_carro=carrito, id_producto=producto_id)

            # Validar y actualizar la cantidad
            nueva_cantidad = int(nueva_cantidad)
            if nueva_cantidad <= 0:
                producto.delete()  # Eliminar si la cantidad es cero o menos
                messages.success(request, "Producto eliminado del carrito.")
            else:
                producto.cantidad_producto = nueva_cantidad
                producto.save()
                messages.success(request, "Cantidad actualizada correctamente.")

        except (CarroDeCompras.DoesNotExist, CarroProducto.DoesNotExist):
            messages.error(request, "Hubo un problema al actualizar el producto.")

    return redirect("mostrar_carrito")


def agregar_al_carrito(request, producto_id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debes iniciar sesión para agregar productos al carrito.")
        return redirect("catalogo")

    try:
        producto = Producto.objects.get(id_producto=producto_id)
        carrito, creado = CarroDeCompras.objects.get_or_create(
            id_usuario_id=usuario_id,
            estado="pendiente",
            defaults={"fecha": date.today(), "cantidad_productos": 0, "precio_total": 0.0},
        )

        # Verificar si el producto ya está en el carrito
        carro_producto, creado = CarroProducto.objects.get_or_create(
            id_carro=carrito, id_producto=producto,
            defaults={"cantidad_producto": 1}
        )
        if not creado:
            # Incrementar la cantidad si ya existe
            carro_producto.cantidad_producto += 1
            carro_producto.save()

        # Actualizar el carrito
        carrito.cantidad_productos = CarroProducto.objects.filter(id_carro=carrito).count()
        carrito.precio_total = sum(
            cp.cantidad_producto * cp.id_producto.precio_producto
            for cp in CarroProducto.objects.filter(id_carro=carrito)
        )
        carrito.save()

        messages.success(request, f"Producto '{producto.nombre_producto}' agregado al carrito.")
    except Producto.DoesNotExist:
        messages.error(request, "El producto no existe.")

    return redirect("catalogo")

def resumen_carrito(request, id_carro):
    carrito = get_object_or_404(CarroDeCompras, pk=id_carro)
    productos = CarroProducto.objects.filter(id_carro=carrito)
    usuario = carrito.id_usuario

    # Calcular el total correctamente, asegurando la precisión con Decimal
    total = sum(
        Decimal(producto.cantidad_producto) * Decimal(producto.id_producto.precio_producto)
        for producto in productos
    )

    # Formatear el total y los precios a formato chileno (sin coma extra)
    total_formateado = f"{total:,.0f}".replace(",", ".")  # Se usa punto como separador de miles

    return render(request, 'resumen.html', {
        'carrito': carrito,
        'productos': productos,
        'usuario': usuario,
        'total': total_formateado,  # Total corregido
    })

def finalizar_compra(request, id_carro):
    if request.method == 'POST':
        metodo_pago = request.POST.get('metodo_pago')
        carrito = get_object_or_404(CarroDeCompras, pk=id_carro)
        productos = CarroProducto.objects.filter(id_carro=carrito)

        # Calcular el total del carrito antes de finalizar
        total = sum(
            Decimal(item.cantidad_producto) * Decimal(item.id_producto.precio_producto)
            for item in productos
        )
        
        # Actualizar el precio total en el carrito
        carrito.precio_total = total
        carrito.estado = 'Finalizado'
        carrito.metodo_pago = metodo_pago
        carrito.fecha = date.today()  # Registrar la fecha actual
        carrito.save()

        # Reducir stock de productos
        for item in productos:
            producto = item.id_producto
            if producto.stock_producto >= item.cantidad_producto:
                producto.stock_producto -= item.cantidad_producto
                producto.save()
            else:
                messages.error(request, f'No hay suficiente stock para el producto {producto.nombre_producto}')
                return redirect('resumen_carrito', id_carro=id_carro)

        messages.success(request, 'Compra finalizada con éxito.')
        return redirect('catalogo')  # Redirige al catálogo u otra página después de finalizar





def perfil(request):
    # Recuperar el usuario desde la sesión
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    # Obtener el usuario
    usuario = Usuario.objects.get(id_usuario=usuario_id)

    # Obtener los carritos finalizados del usuario
    carritos = CarroDeCompras.objects.filter(id_usuario_id=usuario_id, estado='Finalizado')

    # Filtrado por fecha
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    if fecha_inicio:
        carritos = carritos.filter(fecha__gte=datetime.strptime(fecha_inicio, '%Y-%m-%d'))
    if fecha_fin:
        carritos = carritos.filter(fecha__lte=datetime.strptime(fecha_fin, '%Y-%m-%d'))


    # Recopilar los detalles de cada carrito y sus productos
    ventas = []
    for carrito in carritos:
        productos = CarroProducto.objects.filter(id_carro=carrito).select_related('id_producto')

        # Calcular el total de cada carrito
        total = sum(Decimal(item.cantidad_producto) * Decimal(item.id_producto.precio_producto) for item in productos)

        # Preparar detalles de los productos
        detalles_productos = [
            {
                'nombre': producto.id_producto.nombre_producto,
                'cantidad': producto.cantidad_producto,
                'precio': producto.id_producto.precio_producto,
                'subtotal': Decimal(producto.cantidad_producto) * Decimal(producto.id_producto.precio_producto),
                'imagen': producto.id_producto.imagen_producto.url if producto.id_producto.imagen_producto else None
            }
            for producto in productos
        ]

        ventas.append({
            'fecha': carrito.fecha,
            'estado': carrito.estado,
            'cantidad': carrito.cantidad_productos,
            'metodo_pago': carrito.metodo_pago,
            'precio_total': total,
            'productos': detalles_productos
        })

    # Pasar los datos a la plantilla
    data = {
        'usuario': usuario,
        'ventas': ventas,
    }

    return render(request, "perfil.html", data)



def cerrar_sesion(request):
    # Eliminar la sesión
    auth_logout(request)
    # Redirigir al inicio
    return redirect('/')