from django.urls import path
from . import views

app_name = 'ferreteria'

urlpatterns = [
    # Página principal
    path('', views.index, name='index'),
    
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    
    # Catálogo y carrito
    path('catalogo/', views.catalogo, name='catalogo'),
    path('agregar_carrito/<int:articulo_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('actualizar_carrito/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('eliminar_carrito/<int:item_id>/', views.eliminar_carrito, name='eliminar_carrito'),
    path('colocar_pedido/', views.colocar_pedido, name='colocar_pedido'),
    
    # NUEVO: Gestión de pedidos
    path('pedidos/', views.pedido_list, name='pedido_list'),
    path('pedidos/<int:pk>/', views.pedido_detail, name='pedido_detail'),
    path('pedidos/<int:pk>/cambiar_estado/', views.cambiar_estado_pedido, name='cambiar_estado_pedido'),
    path('pedidos/<int:pk>/cancelar/', views.cancelar_pedido, name='cancelar_pedido'),
    
    # NUEVO: Movimientos de inventario
    path('movimientos/', views.movimiento_list, name='movimiento_list'),
    path('movimientos/crear/', views.movimiento_create, name='movimiento_create'),
    path('movimientos/<int:pk>/', views.movimiento_detail, name='movimiento_detail'),
    path('articulos/<int:articulo_id>/movimientos/', views.articulo_movimientos, name='articulo_movimientos'),
    
    # CRUDs - Roles
    path('roles/', views.rol_list, name='rol_list'),
    path('roles/crear/', views.rol_create, name='rol_create'),
    path('roles/<int:pk>/editar/', views.rol_update, name='rol_update'),
    path('roles/<int:pk>/eliminar/', views.rol_delete, name='rol_delete'),
    
    # CRUDs - Empleados
    path('empleados/', views.empleado_list, name='empleado_list'),
    path('empleados/crear/', views.empleado_create, name='empleado_create'),
    path('empleados/<int:pk>/editar/', views.empleado_update, name='empleado_update'),
    path('empleados/<int:pk>/eliminar/', views.empleado_delete, name='empleado_delete'),
    
    # CRUDs - Clientes
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/crear/', views.cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/editar/', views.cliente_update, name='cliente_update'),
    path('clientes/<int:pk>/eliminar/', views.cliente_delete, name='cliente_delete'),
    
    # CRUDs - Proveedores
    path('proveedores/', views.proveedor_list, name='proveedor_list'),
    path('proveedores/crear/', views.proveedor_create, name='proveedor_create'),
    path('proveedores/<int:pk>/editar/', views.proveedor_update, name='proveedor_update'),
    path('proveedores/<int:pk>/eliminar/', views.proveedor_delete, name='proveedor_delete'),
    
    # CRUDs - Categorías
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/crear/', views.categoria_create, name='categoria_create'),
    path('categorias/<int:pk>/editar/', views.categoria_update, name='categoria_update'),
    path('categorias/<int:pk>/eliminar/', views.categoria_delete, name='categoria_delete'),
    
    # CRUDs - Artículos
    path('articulos/', views.articulo_list, name='articulo_list'),
    path('articulos/crear/', views.articulo_create, name='articulo_create'),
    path('articulos/<int:pk>/editar/', views.articulo_update, name='articulo_update'),
    path('articulos/<int:pk>/eliminar/', views.articulo_delete, name='articulo_delete'),
]