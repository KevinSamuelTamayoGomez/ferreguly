from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from .models import Empleado

def login_required(view_func):
    """Decorador para requerir login"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        empleado_id = request.session.get('empleado_id')
        if not empleado_id:
            messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('ferreteria:login')
        
        try:
            empleado = Empleado.objects.get(id=empleado_id, activo=True)
            request.empleado = empleado  # Agregar empleado al request
        except Empleado.DoesNotExist:
            messages.error(request, 'Tu sesión ha expirado.')
            request.session.flush()
            return redirect('ferreteria:login')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def role_required(roles):
    """Decorador para requerir roles específicos"""
    if isinstance(roles, str):
        roles = [roles]
    
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            empleado_id = request.session.get('empleado_id')
            if not empleado_id:
                messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
                return redirect('ferreteria:login')
            
            try:
                empleado = Empleado.objects.get(id=empleado_id, activo=True)
                if empleado.id_rol.nombre not in roles:
                    messages.error(request, f'No tienes permisos para acceder a esta página. Se requiere rol: {", ".join(roles)}')
                    return redirect('ferreteria:index')
                request.empleado = empleado
            except Empleado.DoesNotExist:
                messages.error(request, 'Tu sesión ha expirado.')
                request.session.flush()
                return redirect('ferreteria:login')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def admin_required(view_func):
    """Decorador para requerir rol de Administrador"""
    return role_required(['Administrador', 'Gerente General'])(view_func)