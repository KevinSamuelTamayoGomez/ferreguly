from django.contrib.auth.hashers import make_password, check_password
from .decorators import login_required, role_required, admin_required, cliente_login_required, any_login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from .models import *
from .forms import *

def index(request):
    articulos_destacados = Articulo.objects.filter(activo=True, stock__gt=0)[:6]
    context = {
        'articulos_destacados': articulos_destacados
    }
    return render(request, 'ferreteria/index.html', context)

def catalogo(request):
    articulos = Articulo.objects.filter(activo=True, stock__gt=0)
    categorias = Categoria.objects.all()
    
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        articulos = articulos.filter(id_categoria=categoria_id)
    
    busqueda = request.GET.get('buscar')
    if busqueda:
        articulos = articulos.filter(nombre__icontains=busqueda)
    
    context = {
        'articulos': articulos,
        'categorias': categorias,
        'categoria_seleccionada': int(categoria_id) if categoria_id else None,
        'busqueda': busqueda
    }
    return render(request, 'ferreteria/catalogo.html', context)

@any_login_required
def agregar_carrito(request, articulo_id):
    articulo = get_object_or_404(Articulo, id=articulo_id)
    
    if request.method == 'POST':
        form = AgregarCarritoForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']
            
            if not articulo.activo:
                messages.error(request, f'{articulo.nombre} no está disponible.')
                return redirect('ferreteria:catalogo')
            
            if articulo.stock < cantidad:
                messages.error(request, f'Stock insuficiente para {articulo.nombre}. Disponible: {articulo.stock} unidades.')
                return redirect('ferreteria:catalogo')
            
            # Determinar el propietario del carrito
            if hasattr(request, 'cliente'):
                carrito, created = Carrito.objects.get_or_create(
                    id_cliente=request.cliente,
                    estado='activo',
                    defaults={'id_cliente': request.cliente}
                )
            elif hasattr(request, 'empleado'):
                carrito, created = Carrito.objects.get_or_create(
                    id_empleado=request.empleado,
                    estado='activo',
                    defaults={'id_empleado': request.empleado}
                )
            else:
                messages.error(request, 'Error en la sesión. Inicia sesión nuevamente.')
                return redirect('ferreteria:login_universal')
            
            carrito_item, created = CarritoItem.objects.get_or_create(
                id_carrito=carrito,
                id_articulo=articulo,
                defaults={'cantidad': cantidad}
            )
            
            if not created:
                nueva_cantidad_total = carrito_item.cantidad + cantidad
                if articulo.stock < nueva_cantidad_total:
                    messages.error(request, 
                        f'Stock insuficiente para {articulo.nombre}. '
                        f'Tienes {carrito_item.cantidad} en el carrito, '
                        f'stock disponible: {articulo.stock}, '
                        f'intentas agregar: {cantidad}.'
                    )
                    return redirect('ferreteria:catalogo')
                
                carrito_item.cantidad = nueva_cantidad_total
                carrito_item.save()
                messages.success(request, 
                    f'Se actualizó la cantidad de {articulo.nombre} en el carrito. '
                    f'Total en carrito: {carrito_item.cantidad} unidades.'
                )
            else:
                messages.success(request, f'Se agregó {articulo.nombre} al carrito ({cantidad} unidades).')
            
            return redirect('ferreteria:catalogo')
    
    return redirect('ferreteria:catalogo')

@any_login_required
def ver_carrito(request):
    try:
        if hasattr(request, 'cliente'):
            carrito = Carrito.objects.get(id_cliente=request.cliente, estado='activo')
        elif hasattr(request, 'empleado'):
            carrito = Carrito.objects.get(id_empleado=request.empleado, estado='activo')
        else:
            messages.error(request, 'Error en la sesión.')
            return redirect('ferreteria:login_universal')
            
        items = CarritoItem.objects.filter(id_carrito=carrito)
        total = carrito.get_total()
    except Carrito.DoesNotExist:
        items = []
        total = 0
        carrito = None
    
    context = {
        'items': items,
        'total': total,
        'carrito': carrito
    }
    return render(request, 'ferreteria/carrito.html', context)

@any_login_required
def actualizar_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id)
    
    # Verificar que el item pertenece al usuario actual
    if hasattr(request, 'cliente') and item.id_carrito.id_cliente != request.cliente:
        messages.error(request, 'No tienes permisos para modificar este artículo.')
        return redirect('ferreteria:ver_carrito')
    elif hasattr(request, 'empleado') and item.id_carrito.id_empleado != request.empleado:
        messages.error(request, 'No tienes permisos para modificar este artículo.')
        return redirect('ferreteria:ver_carrito')
    
    if request.method == 'POST':
        form = ActualizarCarritoForm(request.POST)
        if form.is_valid():
            nueva_cantidad = form.cleaned_data['cantidad']
            if item.id_articulo.stock >= nueva_cantidad:
                item.cantidad = nueva_cantidad
                item.save()
                messages.success(request, 'Cantidad actualizada correctamente.')
            else:
                messages.error(request, f'Stock insuficiente. Disponible: {item.id_articulo.stock}')
    
    return redirect('ferreteria:ver_carrito')

@any_login_required
def eliminar_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id)
    
    # Verificar que el item pertenece al usuario actual
    if hasattr(request, 'cliente') and item.id_carrito.id_cliente != request.cliente:
        messages.error(request, 'No tienes permisos para eliminar este artículo.')
        return redirect('ferreteria:ver_carrito')
    elif hasattr(request, 'empleado') and item.id_carrito.id_empleado != request.empleado:
        messages.error(request, 'No tienes permisos para eliminar este artículo.')
        return redirect('ferreteria:ver_carrito')
    
    articulo_nombre = item.id_articulo.nombre
    item.delete()
    messages.success(request, f'Se eliminó {articulo_nombre} del carrito.')
    return redirect('ferreteria:ver_carrito')

@any_login_required
def colocar_pedido(request):
    try:
        if hasattr(request, 'cliente'):
            carrito = Carrito.objects.get(id_cliente=request.cliente, estado='activo')
            cliente = request.cliente
            comprador_empleado = None
        elif hasattr(request, 'empleado'):
            carrito = Carrito.objects.get(id_empleado=request.empleado, estado='activo')
            cliente = None
            comprador_empleado = request.empleado
        else:
            messages.error(request, 'Error en la sesión.')
            return redirect('ferreteria:login_universal')
            
        items = CarritoItem.objects.filter(id_carrito=carrito)
        
        if not items.exists():
            messages.error(request, 'El carrito está vacío.')
            return redirect('ferreteria:ver_carrito')
        
        if request.method == 'POST':
            metodo_pago = request.POST.get('metodo_pago', 'efectivo')
            
            metodos_pago_map = {
                'efectivo': 'Efectivo',
                'tarjeta_debito': 'Tarjeta de Débito',
                'tarjeta_credito': 'Tarjeta de Crédito',
                'transferencia': 'Transferencia Bancaria',
                'cheque': 'Cheque'
            }
            metodo_pago_texto = metodos_pago_map.get(metodo_pago, 'Efectivo')
            
            # Obtener empleado para procesar el pedido
            empleado_procesador = None
            if hasattr(request, 'empleado'):
                empleado_procesador = request.empleado
            else:
                empleado_procesador = Empleado.objects.filter(activo=True).first()
            
            if not empleado_procesador:
                messages.error(request, 'No hay empleados disponibles para procesar el pedido.')
                return redirect('ferreteria:ver_carrito')
            
            with transaction.atomic():
                total = carrito.get_total()
                
                # Determinar dirección de envío
                direccion_envio = ''
                if cliente:
                    direccion_envio = cliente.direccion
                elif comprador_empleado:
                    direccion_envio = request.POST.get('direccion_envio', 'Oficina principal')
                
                pedido = Pedido.objects.create(
                    id_cliente=cliente,
                    id_empleado=empleado_procesador,
                    id_comprador_empleado=comprador_empleado,
                    total=total,
                    estado='pendiente',
                    metodo_pago=metodo_pago_texto,
                    direccion_envio=direccion_envio
                )
                
                for item in items:
                    PedidoDetalle.objects.create(
                        id_pedido=pedido,
                        id_articulo=item.id_articulo,
                        cantidad=item.cantidad,
                        precio_unitario=item.id_articulo.precio
                    )
                    
                    articulo = item.id_articulo
                    articulo.stock -= item.cantidad
                    articulo.save()
                    
                    MovimientoInventario.objects.create(
                        id_articulo=articulo,
                        id_empleado=empleado_procesador,
                        tipo='salida',
                        cantidad=item.cantidad,
                        descripcion=f'Venta automática - Pedido #{pedido.id}'
                    )
                
                Pago.objects.create(
                    id_pedido=pedido,
                    id_empleado=empleado_procesador,
                    monto=total,
                    metodo_pago=metodo_pago_texto
                )
                
                carrito.estado = 'procesado'
                carrito.save()
                items.delete()
                
                messages.success(request, f'Pedido #{pedido.id} creado exitosamente con pago por {metodo_pago_texto}.')
                return render(request, 'ferreteria/pedido_confirmacion.html', {
                    'pedido': pedido,
                    'cliente': cliente,
                    'comprador_empleado': comprador_empleado,
                    'pedido_recien_creado': True
                })
    
    except Carrito.DoesNotExist:
        messages.error(request, 'No tienes un carrito activo.')
        return redirect('ferreteria:catalogo')

def login_universal(request):
    """Vista unificada de login que detecta si es cliente o empleado"""
    if request.session.get('cliente_id') or request.session.get('empleado_id'):
        return redirect('ferreteria:index')
    
    if request.method == 'POST':
        form = LoginUniversalForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            contraseña = form.cleaned_data['contraseña']
            
            # Intentar login como cliente primero
            try:
                cliente = Cliente.objects.get(usuario=usuario, activo=True)
                
                if not cliente.contraseña.startswith('pbkdf2_'):
                    if cliente.contraseña == contraseña:
                        cliente.contraseña = make_password(contraseña)
                        cliente.save()
                        request.session['cliente_id'] = cliente.id
                        request.session['cliente_nombre'] = f"{cliente.nombre} {cliente.apellido}"
                        messages.success(request, f'¡Bienvenido, {cliente.nombre}!')
                        return redirect('ferreteria:index')
                    else:
                        pass  # Continuar con empleado
                else:
                    if check_password(contraseña, cliente.contraseña):
                        request.session['cliente_id'] = cliente.id
                        request.session['cliente_nombre'] = f"{cliente.nombre} {cliente.apellido}"
                        messages.success(request, f'¡Bienvenido, {cliente.nombre}!')
                        return redirect('ferreteria:index')
                    else:
                        pass  # Continuar con empleado
                        
            except Cliente.DoesNotExist:
                pass  # Continuar con empleado
            
            # Intentar login como empleado
            try:
                empleado = Empleado.objects.get(usuario=usuario, activo=True)
                
                if not empleado.contraseña.startswith('pbkdf2_'):
                    if empleado.contraseña == contraseña:
                        empleado.contraseña = make_password(contraseña)
                        empleado.save()
                        request.session['empleado_id'] = empleado.id
                        request.session['empleado_nombre'] = f"{empleado.nombre} {empleado.apellido}"
                        request.session['empleado_rol'] = empleado.id_rol.nombre
                        messages.success(request, f'Bienvenido, {empleado.nombre}!')
                        return redirect('ferreteria:index')
                    else:
                        messages.error(request, 'Usuario o contraseña incorrectos.')
                else:
                    if check_password(contraseña, empleado.contraseña):
                        request.session['empleado_id'] = empleado.id
                        request.session['empleado_nombre'] = f"{empleado.nombre} {empleado.apellido}"
                        request.session['empleado_rol'] = empleado.id_rol.nombre
                        messages.success(request, f'Bienvenido, {empleado.nombre}!')
                        return redirect('ferreteria:index')
                    else:
                        messages.error(request, 'Usuario o contraseña incorrectos.')
                        
            except Empleado.DoesNotExist:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginUniversalForm()
    
    return render(request, 'ferreteria/auth/login_universal.html', {'form': form})

def cliente_register(request):
    if request.method == 'POST':
        form = ClienteRegisterForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.contraseña = make_password(form.cleaned_data['contraseña'])
            cliente.save()
            
            request.session['cliente_id'] = cliente.id
            request.session['cliente_nombre'] = f"{cliente.nombre} {cliente.apellido}"
            messages.success(request, f'¡Cuenta creada exitosamente! Bienvenido, {cliente.nombre}!')
            return redirect('ferreteria:index')
    else:
        form = ClienteRegisterForm()
    
    return render(request, 'ferreteria/auth/cliente_register.html', {'form': form})

def logout_view(request):
    usuario_nombre = request.session.get('cliente_nombre') or request.session.get('empleado_nombre', 'Usuario')
    request.session.flush()
    messages.success(request, f'¡Hasta luego, {usuario_nombre}!')
    return redirect('ferreteria:index')

@cliente_login_required
def cliente_perfil(request):
    cliente = request.cliente
    
    if request.method == 'POST':
        form = ClientePerfilForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            request.session['cliente_nombre'] = f"{cliente.nombre} {cliente.apellido}"
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('ferreteria:cliente_perfil')
    else:
        form = ClientePerfilForm(instance=cliente)
    
    return render(request, 'ferreteria/cliente/perfil.html', {'form': form, 'cliente': cliente})

@cliente_login_required
def cliente_pedidos(request):
    cliente = request.cliente
    pedidos = Pedido.objects.filter(id_cliente=cliente).order_by('-fecha')
    return render(request, 'ferreteria/cliente/pedidos.html', {'pedidos': pedidos})

@cliente_login_required
def cliente_pedido_detail(request, pedido_id):
    cliente = request.cliente
    pedido = get_object_or_404(Pedido, id=pedido_id, id_cliente=cliente)
    detalles = PedidoDetalle.objects.filter(id_pedido=pedido)
    
    context = {
        'pedido': pedido,
        'detalles': detalles,
    }
    return render(request, 'ferreteria/cliente/pedido_detail.html', context)

@login_required
def pedido_list(request):
    pedidos = Pedido.objects.all().order_by('-fecha')
    return render(request, 'ferreteria/pedidos/pedido_list.html', {'pedidos': pedidos})

@login_required  
def pedido_detail(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    detalles = PedidoDetalle.objects.filter(id_pedido=pedido)
    context = {
        'pedido': pedido,
        'detalles': detalles,
    }
    return render(request, 'ferreteria/pedidos/pedido_detail.html', context)

@role_required(['Administrador', 'Gerente General', 'Jefe de Ventas'])
def cambiar_estado_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        pedido.estado = nuevo_estado
        pedido.save()
        messages.success(request, f'Estado del pedido #{pedido.id} actualizado a {pedido.get_estado_display()}.')
        return redirect('ferreteria:pedido_detail', pk=pk)
    
    return redirect('ferreteria:pedido_detail', pk=pk)

@login_required
def cancelar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    
    if pedido.estado != 'pendiente':
        messages.error(request, f'No se puede cancelar el pedido #{pedido.id}. Estado actual: {pedido.get_estado_display()}')
        return redirect('ferreteria:pedido_detail', pk=pk)
    
    if request.method == 'POST':
        empleado_id = request.session.get('empleado_id')
        try:
            empleado = Empleado.objects.get(id=empleado_id, activo=True)
        except Empleado.DoesNotExist:
            messages.error(request, 'Error de sesión. Inicia sesión nuevamente.')
            return redirect('ferreteria:login_universal')
        
        with transaction.atomic():
            detalles = PedidoDetalle.objects.filter(id_pedido=pedido)
            
            for detalle in detalles:
                articulo = detalle.id_articulo
                
                articulo.stock += detalle.cantidad
                articulo.save()
                
                MovimientoInventario.objects.create(
                    id_articulo=articulo,
                    id_empleado=empleado,
                    tipo='entrada',
                    cantidad=detalle.cantidad,
                    descripcion=f'Cancelación de pedido #{pedido.id} - Reversión de stock'
                )
            
            pedido.estado = 'cancelado'
            pedido.save()
            
            messages.success(request, 
                f'Pedido #{pedido.id} cancelado exitosamente. '
                f'Se restauró el stock de {detalles.count()} productos.'
            )
            
        return redirect('ferreteria:pedido_detail', pk=pk)
    
    detalles = PedidoDetalle.objects.filter(id_pedido=pedido)
    context = {
        'pedido': pedido,
        'detalles': detalles,
    }
    return render(request, 'ferreteria/pedidos/cancelar_pedido.html', context)

@login_required
def movimiento_list(request):
    movimientos = MovimientoInventario.objects.all().order_by('-fecha')
    
    if request.GET:
        form = FiltroMovimientosForm(request.GET)
        if form.is_valid():
            if form.cleaned_data['articulo']:
                movimientos = movimientos.filter(id_articulo=form.cleaned_data['articulo'])
            if form.cleaned_data['tipo']:
                movimientos = movimientos.filter(tipo=form.cleaned_data['tipo'])
            if form.cleaned_data['empleado']:
                movimientos = movimientos.filter(id_empleado=form.cleaned_data['empleado'])
            if form.cleaned_data['fecha_desde']:
                movimientos = movimientos.filter(fecha__date__gte=form.cleaned_data['fecha_desde'])
            if form.cleaned_data['fecha_hasta']:
                movimientos = movimientos.filter(fecha__date__lte=form.cleaned_data['fecha_hasta'])
    else:
        form = FiltroMovimientosForm()
    
    total_movimientos = movimientos.count()
    total_entradas = movimientos.filter(tipo='entrada').count()
    total_salidas = movimientos.filter(tipo='salida').count()
    
    context = {
        'movimientos': movimientos,
        'form': form,
        'total_movimientos': total_movimientos,
        'total_entradas': total_entradas,
        'total_salidas': total_salidas,
    }
    return render(request, 'ferreteria/movimientos/movimiento_list.html', context)

@role_required(['Administrador', 'Gerente General', 'Almacenista'])
def movimiento_create(request):
    if request.method == 'POST':
        form = MovimientoInventarioForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.id_empleado = request.empleado
            
            articulo = movimiento.id_articulo
            if movimiento.tipo == 'entrada':
                articulo.stock += movimiento.cantidad
                messages.success(request, f'Entrada registrada: +{movimiento.cantidad} unidades de {articulo.nombre}')
            else:
                if articulo.stock >= movimiento.cantidad:
                    articulo.stock -= movimiento.cantidad
                    messages.success(request, f'Salida registrada: -{movimiento.cantidad} unidades de {articulo.nombre}')
                else:
                    messages.error(request, f'Stock insuficiente. Disponible: {articulo.stock}, Solicitado: {movimiento.cantidad}')
                    return render(request, 'ferreteria/movimientos/movimiento_form.html', {'form': form, 'titulo': 'Registrar Movimiento'})
            
            articulo.save()
            movimiento.save()
            return redirect('ferreteria:movimiento_list')
    else:
        form = MovimientoInventarioForm()
    
    return render(request, 'ferreteria/movimientos/movimiento_form.html', {'form': form, 'titulo': 'Registrar Movimiento'})

@login_required
def movimiento_detail(request, pk):
    movimiento = get_object_or_404(MovimientoInventario, pk=pk)
    return render(request, 'ferreteria/movimientos/movimiento_detail.html', {'movimiento': movimiento})

@login_required
def articulo_movimientos(request, articulo_id):
    articulo = get_object_or_404(Articulo, pk=articulo_id)
    movimientos = MovimientoInventario.objects.filter(id_articulo=articulo).order_by('-fecha')
    
    context = {
        'articulo': articulo,
        'movimientos': movimientos,
    }
    return render(request, 'ferreteria/movimientos/articulo_movimientos.html', context)

@admin_required
def rol_list(request):
    roles = Rol.objects.all()
    return render(request, 'ferreteria/crud/rol_list.html', {'roles': roles})

@admin_required
def rol_create(request):
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rol creado exitosamente.')
            return redirect('ferreteria:rol_list')
    else:
        form = RolForm()
    return render(request, 'ferreteria/crud/rol_form.html', {'form': form, 'titulo': 'Crear Rol'})

@admin_required
def rol_update(request, pk):
    rol = get_object_or_404(Rol, pk=pk)
    if request.method == 'POST':
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rol actualizado exitosamente.')
            return redirect('ferreteria:rol_list')
    else:
        form = RolForm(instance=rol)
    return render(request, 'ferreteria/crud/rol_form.html', {'form': form, 'titulo': 'Editar Rol'})

@admin_required
def rol_delete(request, pk):
    rol = get_object_or_404(Rol, pk=pk)
    if request.method == 'POST':
        rol.delete()
        messages.success(request, 'Rol eliminado exitosamente.')
        return redirect('ferreteria:rol_list')
    return render(request, 'ferreteria/crud/rol_list.html', {'roles': Rol.objects.all()})

@admin_required
def empleado_list(request):
    empleados = Empleado.objects.all()
    return render(request, 'ferreteria/crud/empleado_list.html', {'empleados': empleados})

@admin_required
def empleado_create(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado creado exitosamente.')
            return redirect('ferreteria:empleado_list')
    else:
        form = EmpleadoForm()
    return render(request, 'ferreteria/crud/empleado_form.html', {'form': form, 'titulo': 'Crear Empleado'})

@admin_required
def empleado_update(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado actualizado exitosamente.')
            return redirect('ferreteria:empleado_list')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'ferreteria/crud/empleado_form.html', {'form': form, 'titulo': 'Editar Empleado'})

@admin_required
def empleado_delete(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        messages.success(request, 'Empleado eliminado exitosamente.')
        return redirect('ferreteria:empleado_list')
    return render(request, 'ferreteria/crud/empleado_list.html', {'empleados': Empleado.objects.all()})

@role_required(['Administrador', 'Gerente General', 'Jefe de Ventas', 'Vendedor'])
def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'ferreteria/crud/cliente_list.html', {'clientes': clientes})

@role_required(['Administrador', 'Gerente General', 'Jefe de Ventas', 'Vendedor'])
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.contraseña = make_password(cliente.contraseña)
            cliente.save()
            messages.success(request, 'Cliente creado exitosamente.')
            return redirect('ferreteria:cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'ferreteria/crud/cliente_form.html', {'form': form, 'titulo': 'Crear Cliente'})

@role_required(['Administrador', 'Gerente General', 'Jefe de Ventas', 'Vendedor'])
def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save(commit=False)
            if not cliente.contraseña.startswith('pbkdf2_'):
                cliente.contraseña = make_password(cliente.contraseña)
            cliente.save()
            messages.success(request, 'Cliente actualizado exitosamente.')
            return redirect('ferreteria:cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'ferreteria/crud/cliente_form.html', {'form': form, 'titulo': 'Editar Cliente'})

@role_required(['Administrador', 'Gerente General', 'Jefe de Ventas'])
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado exitosamente.')
        return redirect('ferreteria:cliente_list')
    return render(request, 'ferreteria/crud/cliente_list.html', {'clientes': Cliente.objects.all()})

@role_required(['Administrador', 'Gerente General', 'Almacenista'])
def proveedor_list(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'ferreteria/crud/proveedor_list.html', {'proveedores': proveedores})

@role_required(['Administrador', 'Gerente General', 'Almacenista'])
def proveedor_create(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor creado exitosamente.')
            return redirect('ferreteria:proveedor_list')
    else:
        form = ProveedorForm()
    return render(request, 'ferreteria/crud/proveedor_form.html', {'form': form, 'titulo': 'Crear Proveedor'})

@role_required(['Administrador', 'Gerente General', 'Almacenista'])
def proveedor_update(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor actualizado exitosamente.')
            return redirect('ferreteria:proveedor_list')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'ferreteria/crud/proveedor_form.html', {'form': form, 'titulo': 'Editar Proveedor'})

@admin_required
def proveedor_delete(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        messages.success(request, 'Proveedor eliminado exitosamente.')
        return redirect('ferreteria:proveedor_list')
    return render(request, 'ferreteria/crud/proveedor_list.html', {'proveedores': Proveedor.objects.all()})

@role_required(['Administrador', 'Gerente General', 'Almacenista'])
def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'ferreteria/crud/categoria_list.html', {'categorias': categorias})

@role_required(['Administrador', 'Gerente General', 'Almacenista'])
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('ferreteria:categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'ferreteria/crud/categoria_form.html', {'form': form, 'titulo': 'Crear Categoría'})

@role_required(['Administrador', 'Gerente General', 'Almacenista'])
def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente.')
            return redirect('ferreteria:categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'ferreteria/crud/categoria_form.html', {'form': form, 'titulo': 'Editar Categoría'})

@admin_required
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada exitosamente.')
        return redirect('ferreteria:categoria_list')
    return render(request, 'ferreteria/crud/categoria_list.html', {'categorias': Categoria.objects.all()})

@login_required
def articulo_list(request):
    articulos = Articulo.objects.all()
    return render(request, 'ferreteria/crud/articulo_list.html', {'articulos': articulos})

@role_required(['Administrador', 'Gerente General', 'Almacenista'])
def articulo_create(request):
    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artículo creado exitosamente.')
            return redirect('ferreteria:articulo_list')
    else:
        form = ArticuloForm()
    return render(request, 'ferreteria/crud/articulo_form.html', {'form': form, 'titulo': 'Crear Artículo'})

@role_required(['Administrador', 'Gerente General', 'Almacenista'])
def articulo_update(request, pk):
    articulo = get_object_or_404(Articulo, pk=pk)
    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES, instance=articulo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artículo actualizado exitosamente.')
            return redirect('ferreteria:articulo_list')
    else:
        form = ArticuloForm(instance=articulo)
    return render(request, 'ferreteria/crud/articulo_form.html', {'form': form, 'titulo': 'Editar Artículo'})

@admin_required
def articulo_delete(request, pk):
    articulo = get_object_or_404(Articulo, pk=pk)
    if request.method == 'POST':
        articulo.delete()
        messages.success(request, 'Artículo eliminado exitosamente.')
        return redirect('ferreteria:articulo_list')
    return render(request, 'ferreteria/crud/articulo_list.html', {'articulos': Articulo.objects.all()})

def login(request):
    """Vista de login solo para empleados (compatible con sistema anterior)"""
    return login_universal(request)

@login_required
def perfil_view(request):
    empleado = request.empleado
    return render(request, 'ferreteria/auth/perfil.html', {'empleado': empleado})