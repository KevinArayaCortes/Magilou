# Generated by Django 3.2 on 2024-11-19 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarroDeCompras',
            fields=[
                ('id_carro', models.CharField(max_length=18, primary_key=True, serialize=False)),
                ('cantidad_productos', models.IntegerField(blank=True, null=True)),
                ('fecha', models.DateField()),
                ('precio_total', models.FloatField(blank=True, null=True)),
                ('estado', models.CharField(blank=True, max_length=20, null=True)),
                ('metodo_pago', models.CharField(blank=True, max_length=18, null=True)),
            ],
            options={
                'db_table': 'Carro_de_compras',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.CharField(max_length=18, primary_key=True, serialize=False)),
                ('nombre_producto', models.CharField(max_length=20)),
                ('tipo_producto', models.CharField(max_length=20)),
                ('descripcion_producto', models.CharField(max_length=20)),
                ('precio_producto', models.FloatField()),
                ('stock_producto', models.IntegerField()),
            ],
            options={
                'db_table': 'Producto',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id_usuario', models.CharField(max_length=18, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=20)),
                ('apellido', models.CharField(max_length=18)),
                ('rut', models.CharField(max_length=20)),
                ('correo', models.CharField(max_length=20)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'Usuario',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CarroProducto',
            fields=[
                ('id_carro', models.OneToOneField(db_column='id_carro', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='AppMagilou.carrodecompras')),
                ('cantidad_producto', models.IntegerField()),
            ],
            options={
                'db_table': 'Carro_Producto',
                'managed': False,
            },
        ),
    ]
