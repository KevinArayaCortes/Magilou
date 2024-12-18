"""magilou URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AppMagilou import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path("mostrar_carrito/", views.mostrar_carrito, name="mostrar_carrito"),
    path("eliminar_producto/<int:producto_id>/", views.eliminar_producto_carrito, name="eliminar_producto"),
    path("actualizar_cantidad/<int:producto_id>/", views.actualizar_cantidad_producto, name="actualizar_cantidad"),
    path("agregar_al_carrito/<int:producto_id>/", views.agregar_al_carrito, name="agregar_al_carrito"),
    path('resumen_carrito/<int:id_carro>/', views.resumen_carrito, name='resumen_carrito'),
    path('finalizar_compra/<int:id_carro>/', views.finalizar_compra, name='finalizar_compra'),
    path('perfil/', views.perfil, name='perfil'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),

]