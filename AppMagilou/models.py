from django.db import models


class Usuario(models.Model):
    id_usuario = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    rut = models.CharField(max_length=20, unique=True)
    correo = models.EmailField(max_length=50, unique=True)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    contrasena = models.CharField(max_length=255)
    class Meta:
        db_table = 'Usuario'


class Producto(models.Model):
    id_producto = models.BigAutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=20)
    tipo_producto = models.CharField(max_length=20)
    descripcion_producto = models.CharField(max_length=100)
    precio_producto = models.FloatField()
    stock_producto = models.IntegerField()

    class Meta:
        db_table = 'Producto'


class CarroDeCompras(models.Model):
    id_carro = models.BigAutoField(primary_key=True)
    cantidad_productos = models.IntegerField(blank=True, null=True)
    fecha = models.DateField(auto_now_add=True)
    id_usuario = models.ForeignKey(
        'Usuario',
        on_delete=models.CASCADE,
        db_column='id_usuario',
        related_name='carros'
    )
    precio_total = models.FloatField(blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    metodo_pago = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'Carro_de_compras'


class CarroProducto(models.Model):
    id_producto = models.ForeignKey(
        'Producto',
        on_delete=models.CASCADE,
        db_column='id_producto'
    )
    id_carro = models.ForeignKey(
        'CarroDeCompras',
        on_delete=models.CASCADE,
        db_column='id_carro'
    )
    cantidad_producto = models.IntegerField()

    class Meta:
        db_table = 'Carro_Producto'
        unique_together = (('id_carro', 'id_producto'),)