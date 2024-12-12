# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has on_delete set to the desired behavior
#   * Remove managed = False lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from decimal import Decimal

class CarroProducto(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_producto = models.ForeignKey('Producto', models.DO_NOTHING, db_column='id_producto')
    id_carro = models.ForeignKey('CarroDeCompras', models.DO_NOTHING, db_column='id_carro')
    cantidad_producto = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Carro_Producto'
        unique_together = (('id_carro', 'id_producto'),)


class CarroDeCompras(models.Model):
    id_carro = models.BigAutoField(primary_key=True)
    cantidad_productos = models.IntegerField(blank=True, null=True)
    fecha = models.DateField()
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario')
    precio_total = models.FloatField(blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    metodo_pago = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Carro_de_compras'


class Producto(models.Model):
    id_producto = models.BigAutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=20)
    tipo_producto = models.CharField(max_length=20)
    descripcion_producto = models.CharField(max_length=100)
    precio_producto = models.DecimalField(max_digits=12, decimal_places=0)  # Máximo 12 dígitos, sin decimales
    stock_producto = models.IntegerField()
    imagen_producto = models.ImageField(upload_to='productos/', blank=True, null=True)  # Se subirá al bucket S3

    def format_precio(self):
        return f"${self.precio_producto:,.0f}".replace(",", ".")  # Formato chileno

    def __str__(self):
        return f"{self.nombre_producto} - {self.format_precio()}"

    class Meta:
        managed = True
        db_table = 'Producto'




class Usuario(models.Model):
    id_usuario = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    rut = models.CharField(max_length=20)
    correo = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    contrasena = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Usuario'