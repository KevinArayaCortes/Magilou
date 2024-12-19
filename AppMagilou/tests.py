from django.test import TestCase, Client
from django.urls import reverse
from AppMagilou.models import Usuario, Producto, CarroDeCompras, CarroProducto
from datetime import date

class AppMagilouTests(TestCase):
    def setUp(self):
        # Configurar datos iniciales
        self.client = Client()

        # Crear un usuario
        self.usuario = Usuario.objects.create(
            nombre="Juan",
            apellido="Pérez",
            rut="12345678-9",
            correo="juan@example.com",
            direccion="Calle Falsa 123",
            telefono="123456789",
            contrasena="hashedpassword123"
        )

        # Crear productos
        self.producto1 = Producto.objects.create(
            nombre_producto="Producto 1",
            tipo_producto="Tipo 1",
            descripcion_producto="Descripción del producto 1",
            precio_producto=10000,
            stock_producto=10
        )
        self.producto2 = Producto.objects.create(
            nombre_producto="Producto 2",
            tipo_producto="Tipo 2",
            descripcion_producto="Descripción del producto 2",
            precio_producto=15000,
            stock_producto=5
        )

    def test_home_view(self):
        # Probar carga del home
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_catalogo_view(self):
        # Probar la vista del catálogo
        response = self.client.get(reverse('catalogo'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogo.html')
        self.assertIn("Producto 1", str(response.content))
        self.assertIn("Producto 2", str(response.content))

    def test_agregar_al_carrito(self):
        # Simular inicio de sesión
        session = self.client.session
        session['usuario_id'] = self.usuario.id_usuario
        session.save()

        # Agregar un producto al carrito
        response = self.client.get(reverse('agregar_al_carrito', args=[self.producto1.id_producto]))
        self.assertEqual(response.status_code, 302)  # Redirección al catálogo

        # Verificar que el carrito se haya creado
        carrito = CarroDeCompras.objects.get(id_usuario=self.usuario, estado="pendiente")
        self.assertEqual(carrito.cantidad_productos, 1)

    def test_mostrar_carrito(self):
        # Configurar un carrito con productos
        carrito = CarroDeCompras.objects.create(
            id_usuario=self.usuario,
            fecha=date.today(),
            estado="pendiente"
        )
        CarroProducto.objects.create(
            id_carro=carrito,
            id_producto=self.producto1,
            cantidad_producto=2
        )

        # Probar la vista del carrito
        session = self.client.session
        session['usuario_id'] = self.usuario.id_usuario
        session.save()

        response = self.client.get(reverse('mostrar_carrito'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Producto 1", str(response.content))

    def test_finalizar_compra(self):
        # Configurar un carrito con productos
        carrito = CarroDeCompras.objects.create(
            id_usuario=self.usuario,
            fecha=date.today(),
            estado="pendiente"
        )
        CarroProducto.objects.create(
            id_carro=carrito,
            id_producto=self.producto1,
            cantidad_producto=2
        )

        # Finalizar la compra
        response = self.client.post(reverse('finalizar_compra', args=[carrito.id_carro]), data={
            'metodo_pago': 'Tarjeta'
        })
        self.assertEqual(response.status_code, 302)  # Redirección tras finalizar
        carrito.refresh_from_db()
        self.assertEqual(carrito.estado, "Finalizado")
        self.assertEqual(carrito.metodo_pago, "Tarjeta")

