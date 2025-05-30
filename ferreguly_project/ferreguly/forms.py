from django import forms
from .models import *

# ===============================================
# FORMULARIOS DE AUTENTICACIÓN (SISTEMA DUAL)
# ===============================================

class LoginUniversalForm(forms.Form):
    usuario = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Usuario',
            'autofocus': True
        }),
        label='Usuario'
    )
    
    contraseña = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        }),
        label='Contraseña'
    )

class ClienteRegisterForm(forms.ModelForm):
    contraseña = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        }),
        label='Contraseña'
    )
    
    confirmar_contraseña = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        }),
        label='Confirmar Contraseña'
    )
    
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono', 'email', 'direccion', 'usuario']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        contraseña = cleaned_data.get('contraseña')
        confirmar_contraseña = cleaned_data.get('confirmar_contraseña')
        
        if contraseña and confirmar_contraseña:
            if contraseña != confirmar_contraseña:
                raise forms.ValidationError('Las contraseñas no coinciden.')
        
        return cleaned_data

class ClientePerfilForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono', 'email', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }

# ===============================================
# FORMULARIOS CRUD BÁSICOS
# ===============================================

class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'apellido', 'cargo', 'telefono', 'email', 'usuario', 'contraseña', 'id_rol', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'usuario': forms.TextInput(attrs={'class': 'form-control'}),
            'contraseña': forms.PasswordInput(attrs={'class': 'form-control'}),
            'id_rol': forms.Select(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono', 'email', 'direccion', 'usuario', 'contraseña', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario': forms.TextInput(attrs={'class': 'form-control'}),
            'contraseña': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'telefono', 'direccion', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['codigo_sku', 'nombre', 'descripcion', 'precio', 'stock', 'id_categoria', 'id_proveedor', 'imagen_url', 'activo']
        widgets = {
            'codigo_sku': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'id_categoria': forms.Select(attrs={'class': 'form-control'}),
            'id_proveedor': forms.Select(attrs={'class': 'form-control'}),
            'imagen_url': forms.FileInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# ===============================================
# FORMULARIOS DEL CARRITO (ACTUALIZADOS)
# ===============================================

class AgregarCarritoForm(forms.Form):
    cantidad = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'value': 1,
            'min': 1
        }),
        label='Cantidad'
    )

class ActualizarCarritoForm(forms.Form):
    cantidad = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1
        }),
        label='Cantidad'
    )

# ===============================================
# FORMULARIOS DE PEDIDOS
# ===============================================

class MetodoPagoForm(forms.Form):
    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('tarjeta_debito', 'Tarjeta de Débito'),
        ('tarjeta_credito', 'Tarjeta de Crédito'),
        ('transferencia', 'Transferencia Bancaria'),
        ('cheque', 'Cheque'),
    ]
    
    metodo_pago = forms.ChoiceField(
        choices=METODOS_PAGO,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Método de Pago'
    )
    
    direccion_envio = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Dirección de Envío',
        required=False,
        help_text='Déjalo vacío para usar la dirección registrada'
    )

# ===============================================
# FORMULARIOS DE MOVIMIENTOS DE INVENTARIO
# ===============================================

class MovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['id_articulo', 'tipo', 'cantidad', 'descripcion']
        widgets = {
            'id_articulo': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Motivo del movimiento'}),
        }
        labels = {
            'id_articulo': 'Artículo',
            'tipo': 'Tipo de Movimiento',
            'cantidad': 'Cantidad',
            'descripcion': 'Descripción/Motivo'
        }

class FiltroMovimientosForm(forms.Form):
    TIPO_CHOICES = [
        ('', 'Todos los tipos'),
        ('entrada', 'Entradas'),
        ('salida', 'Salidas'),
    ]
    
    articulo = forms.ModelChoiceField(
        queryset=Articulo.objects.filter(activo=True),
        required=False,
        empty_label="Todos los artículos",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    tipo = forms.ChoiceField(
        choices=TIPO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    empleado = forms.ModelChoiceField(
        queryset=Empleado.objects.filter(activo=True),
        required=False,
        empty_label="Todos los empleados",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )