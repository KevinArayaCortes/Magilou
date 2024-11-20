from django.contrib import admin
from AppMagilou.models import CarroDeCompras, CarroProducto, Producto, Usuario

# Configuración para CarroDeCompras
class CarroDeComprasAdmin(admin.ModelAdmin):
    list_display = ('id_carro', 'fecha', 'id_usuario', 'precio_total', 'estado', 'metodo_pago')
    search_fields = ('id_carro', 'estado')
    list_filter = ('estado', 'metodo_pago')
    date_hierarchy = 'fecha'

# Configuración para CarroProducto
class CarroProductoAdmin(admin.ModelAdmin):
    list_display = ('id_carro', 'id_producto', 'cantidad_producto')
    search_fields = ('id_carro__id_carro', 'id_producto__nombre_producto')  # Uso de campos relacionados para búsqueda

# Configuración para Producto
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'nombre_producto', 'tipo_producto', 'precio_producto', 'stock_producto')
    search_fields = ('nombre_producto', 'tipo_producto')
    list_filter = ('tipo_producto',)
    ordering = ('nombre_producto',)

# Configuración para Usuario
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'nombre', 'apellido', 'rut', 'correo', 'telefono', 'contrasena')
    search_fields = ('nombre', 'apellido', 'rut', 'correo')
    list_filter = ('direccion',)
    ordering = ('apellido', 'nombre')

# Registro de modelos en el admin
admin.site.register(CarroDeCompras, CarroDeComprasAdmin)
admin.site.register(CarroProducto, CarroProductoAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Usuario, UsuarioAdmin)
