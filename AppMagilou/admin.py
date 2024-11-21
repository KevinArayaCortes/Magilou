from django.contrib import admin
from AppMagilou.models import CarroProducto, CarroDeCompras, Producto, Usuario

# Personalización del modelo Usuario
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'nombre', 'apellido', 'rut', 'correo', 'telefono')
    search_fields = ('nombre', 'apellido', 'rut', 'correo')
    list_filter = ('direccion',)
    ordering = ('id_usuario',)


# Personalización del modelo Producto
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre_producto', 'precio_producto', 'stock_producto', 'imagen_producto')
    search_fields = ('nombre_producto', 'tipo_producto')
    list_filter = ('tipo_producto',)
    ordering = ('id_producto',)


# Personalización del modelo CarroDeCompras
@admin.register(CarroDeCompras)
class CarroDeComprasAdmin(admin.ModelAdmin):
    list_display = ('id_carro', 'id_usuario', 'cantidad_productos', 'precio_total', 'estado', 'metodo_pago', 'fecha')
    search_fields = ('id_usuario__nombre', 'id_usuario__apellido', 'estado', 'metodo_pago')
    list_filter = ('estado', 'metodo_pago', 'fecha')
    ordering = ('id_carro',)
    date_hierarchy = 'fecha'


# Personalización del modelo CarroProducto
@admin.register(CarroProducto)
class CarroProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_carro', 'id_producto', 'cantidad_producto')
    search_fields = ('id_carro__id_usuario__nombre', 'id_producto__nombre_producto')
    ordering = ('id',)
