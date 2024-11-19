from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from django.db.models import Sum, F
from django.dispatch import receiver
from .models import CarroProducto, Producto, CarroDeCompras, Usuario

# Actualizar el stock del producto al agregar un producto al carro
@receiver(post_save, sender=CarroProducto)
def actualizar_stock_producto(sender, instance, created, **kwargs):
    if created:  # Si se crea un nuevo registro de CarroProducto
        producto = instance.id_producto
        producto.stock_producto -= instance.cantidad_producto
        producto.save()
        actualizar_precio_total(instance.id_carro)

# Revertir el stock del producto al eliminar un producto del carro
@receiver(post_delete, sender=CarroProducto)
def revertir_stock_producto(sender, instance, **kwargs):
    producto = instance.id_producto
    producto.stock_producto += instance.cantidad_producto
    producto.save()
    actualizar_precio_total(instance.id_carro)

# Actualizar el precio total del carro al agregar o eliminar productos
def actualizar_precio_total(carro_id):
    precio_total_actualizado = CarroProducto.objects.filter(
        id_carro=carro_id
    ).aggregate(
        total=Sum(F("cantidad_producto") * F("id_producto__precio_producto"))
    )["total"] or 0  # Si no hay productos, el total será 0
    carro = CarroDeCompras.objects.get(pk=carro_id.pk)
    carro.precio_total = precio_total_actualizado
    carro.save()

# Prevenir la eliminación de un usuario con carros de compras asociados
@receiver(pre_delete, sender=Usuario)
def prevenir_eliminacion_usuario(sender, instance, **kwargs):
    if CarroDeCompras.objects.filter(id_usuario=instance.pk).exists():
        raise ValueError("No se puede eliminar un usuario con carros de compras asociados.")

# Prevenir la eliminación de un carro que tenga productos asociados
@receiver(pre_delete, sender=CarroDeCompras)
def prevenir_eliminacion_carro(sender, instance, **kwargs):
    if CarroProducto.objects.filter(id_carro=instance.pk).exists():
        raise ValueError("No se puede eliminar un carro con productos asociados.")

# Verificar actualización del precio de los productos y actualizar los carros correspondientes
@receiver(pre_save, sender=Producto)
def verificar_actualizacion_precio_producto(sender, instance, **kwargs):
    if instance.pk:  # Si el producto ya existe
        producto_anterior = Producto.objects.get(pk=instance.pk)
        if producto_anterior.precio_producto != instance.precio_producto:
            carros = CarroProducto.objects.filter(id_producto=instance.pk).values(
                "id_carro"
            )
            for carro in carros:
                carro_id = carro["id_carro"]
                carro_obj = CarroDeCompras.objects.get(pk=carro_id)
                precio_total_actualizado = CarroProducto.objects.filter(
                    id_carro=carro_obj
                ).aggregate(
                    total=Sum(F("cantidad_producto") * F("id_producto__precio_producto"))
                )["total"]
                carro_obj.precio_total = precio_total_actualizado
                carro_obj.save()
