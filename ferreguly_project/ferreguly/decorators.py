from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from .models import Empleado, Cliente

def login_required(view_func):
    """Decorador para requerir login de empleado"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('empleado_id'):
            messages.error(request, 'Debes iniciar sesión como empleado para acceder a esta página.')
            return redirect('ferreteria:login')
        
        try:
            empleado = Empleado.objects.get(id=request.session['empleado_id'], activo=True)
            request.empleado = empleado
        except Empleado.DoesNotExist:
            request.session.flush()
            messages.error(request, 'Sesión inválida. Inicia sesión nuevamente.')
            return redirect('ferreteria:login')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper

def cliente_login_required(view_func):
    """Decorador para requerir login de cliente"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('cliente_id'):
            messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('ferreteria:cliente_login')
        
        try:
            cliente = Cliente.objects.get(id=request.session['cliente_id'], activo=True)
            request.cliente = cliente
        except Cliente.DoesNotExist:
            request.session.flush()
            messages.error(request, 'Sesión inválida. Inicia sesión nuevamente.')
            return redirect('ferreteria:cliente_login')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper

def any_login_required(view_func):
    """Decorador para requerir login de cliente O empleado"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verificar si hay login de cliente
        if request.session.get('cliente_id'):
            try:
                cliente = Cliente.objects.get(id=request.session['cliente_id'], activo=True)
                request.cliente = cliente
                request.user_type = 'cliente'
                return view_func(request, *args, **kwargs)
            except Cliente.DoesNotExist:
                request.session.pop('cliente_id', None)
                request.session.pop('cliente_nombre', None)
        
        # Verificar si hay login de empleado
        if request.session.get('empleado_id'):
            try:
                empleado = Empleado.objects.get(id=request.session['empleado_id'], activo=True)
                request.empleado = empleado
                request.user_type = 'empleado'
                return view_func(request, *args, **kwargs)
            except Empleado.DoesNotExist:
                request.session.pop('empleado_id', None)
                request.session.pop('empleado_nombre', None)
                request.session.pop('empleado_rol', None)
        
        # Si no hay ningún login válido
        messages.error(request, 'Debes iniciar sesión para realizar compras.')
        return redirect('ferreteria:login_universal')
        
    return wrapper

def role_required(allowed_roles):
    """Decorador para requerir roles específicos de empleado"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.session.get('empleado_id'):
                messages.error(request, 'Debes iniciar sesión como empleado para acceder a esta página.')
                return redirect('ferreteria:login')
            
            try:
                empleado = Empleado.objects.get(id=request.session['empleado_id'], activo=True)
                request.empleado = empleado
                
                if empleado.id_rol.nombre not in allowed_roles:
                    messages.error(request, f'No tienes permisos para acceder a esta página. Se requiere rol: {", ".join(allowed_roles)}')
                    return redirect('ferreteria:index')
                    
            except Empleado.DoesNotExist:
                request.session.flush()
                messages.error(request, 'Sesión inválida. Inicia sesión nuevamente.')
                return redirect('ferreteria:login')
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator

def admin_required(view_func):
    """Decorador para requerir permisos de administrador"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('empleado_id'):
            messages.error(request, 'Debes iniciar sesión como administrador para acceder a esta página.')
            return redirect('ferreteria:login')
        
        try:
            empleado = Empleado.objects.get(id=request.session['empleado_id'], activo=True)
            request.empleado = empleado
            
            if empleado.id_rol.nombre != 'Administrador':
                messages.error(request, 'Solo los administradores pueden acceder a esta página.')
                return redirect('ferreteria:index')
                
        except Empleado.DoesNotExist:
            request.session.flush()
            messages.error(request, 'Sesión inválida. Inicia sesión nuevamente.')
            return redirect('ferreteria:login')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper