from django.urls import path
from . import views

app_name = 'ferreteria'

urlpatterns = [
    # Páginas públicas
    path('', views.index, name='index'),
    path('catalogo/', views.catalogo, name='catalogo'),
    
    # Autenticación universal
    path('login/', views.login_universal, name='login_universal'),
    path('login/empleado/', views.login, name='login'), # Compatibilidad
    path('registro/', views.cliente_register, name='cliente_register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Carrito (requiere login)
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:articulo_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/actualizar/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_carrito, name='eliminar_carrito'),
    path('pedido/crear/', views.colocar_pedido, name='colocar_pedido'),
    
    # Perfil de cliente
    path('cliente/perfil/', views.cliente_perfil, name='cliente_perfil'),
    path('cliente/pedidos/', views.cliente_pedidos, name='cliente_pedidos'),
    path('cliente/pedidos/<int:pedido_id>/', views.cliente_pedido_detail, name='cliente_pedido_detail'),
    
    # Gestión de pedidos (empleados)
    path('pedidos/', views.pedido_list, name='pedido_list'),
    path('pedidos/<int:pk>/', views.pedido_detail, name='pedido_detail'),
    path('pedidos/<int:pk>/cambiar-estado/', views.cambiar_estado_pedido, name='cambiar_estado_pedido'),
    path('pedidos/<int:pk>/cancelar/', views.cancelar_pedido, name='cancelar_pedido'),
    
    # Movimientos de inventario
    path('movimientos/', views.movimiento_list, name='movimiento_list'),
    path('movimientos/crear/', views.movimiento_create, name='movimiento_create'),
    path('movimientos/<int:pk>/', views.movimiento_detail, name='movimiento_detail'),
    path('articulos/<int:articulo_id>/movimientos/', views.articulo_movimientos, name='articulo_movimientos'),
    
    # CRUD Roles
    path('roles/', views.rol_list, name='rol_list'),
    path('roles/crear/', views.rol_create, name='rol_create'),
    path('roles/<int:pk>/editar/', views.rol_update, name='rol_update'),
    path('roles/<int:pk>/eliminar/', views.rol_delete, name='rol_delete'),
    
    # CRUD Empleados
    path('empleados/', views.empleado_list, name='empleado_list'),
    path('empleados/crear/', views.empleado_create, name='empleado_create'),
    path('empleados/<int:pk>/editar/', views.empleado_update, name='empleado_update'),
    path('empleados/<int:pk>/eliminar/', views.empleado_delete, name='empleado_delete'),
    path('empleados/perfil/', views.perfil_view, name='perfil_view'),
    
    # CRUD Clientes
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/crear/', views.cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/editar/', views.cliente_update, name='cliente_update'),
    path('clientes/<int:pk>/eliminar/', views.cliente_delete, name='cliente_delete'),
    
    # CRUD Proveedores
    path('proveedores/', views.proveedor_list, name='proveedor_list'),
    path('proveedores/crear/', views.proveedor_create, name='proveedor_create'),
    path('proveedores/<int:pk>/editar/', views.proveedor_update, name='proveedor_update'),
    path('proveedores/<int:pk>/eliminar/', views.proveedor_delete, name='proveedor_delete'),
    
    # CRUD Categorías
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/crear/', views.categoria_create, name='categoria_create'),
    path('categorias/<int:pk>/editar/', views.categoria_update, name='categoria_update'),
    path('categorias/<int:pk>/eliminar/', views.categoria_delete, name='categoria_delete'),
    
    # CRUD Artículos
    path('articulos/', views.articulo_list, name='articulo_list'),
    path('articulos/crear/', views.articulo_create, name='articulo_create'),
    path('articulos/<int:pk>/editar/', views.articulo_update, name='articulo_update'),
    path('articulos/<int:pk>/eliminar/', views.articulo_delete, name='articulo_delete'),
]