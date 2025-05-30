from django.contrib import admin
from .models import *

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'cargo', 'telefono', 'email', 'activo']
    list_filter = ['activo', 'id_rol', 'cargo']
    search_fields = ['nombre', 'apellido', 'email']

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'telefono', 'email', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre', 'apellido', 'email']

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'telefono', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo_sku', 'precio', 'stock', 'id_categoria', 'activo']
    list_filter = ['activo', 'id_categoria', 'id_proveedor']
    search_fields = ['nombre', 'codigo_sku']

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_cliente', 'estado', 'fecha_creacion']
    list_filter = ['estado']

@admin.register(CarritoItem)
class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ['id_carrito', 'id_articulo', 'cantidad']

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_cliente', 'estado', 'total', 'fecha']
    list_filter = ['estado', 'fecha']
    search_fields = ['id_cliente__nombre', 'id_cliente__apellido']

@admin.register(PedidoDetalle)
class PedidoDetalleAdmin(admin.ModelAdmin):
    list_display = ['id_pedido', 'id_articulo', 'cantidad', 'precio_unitario']

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ['id_articulo', 'tipo', 'cantidad', 'fecha', 'id_empleado']
    list_filter = ['tipo', 'fecha']

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['id_pedido', 'monto', 'metodo_pago', 'fecha']
    list_filter = ['metodo_pago', 'fecha']