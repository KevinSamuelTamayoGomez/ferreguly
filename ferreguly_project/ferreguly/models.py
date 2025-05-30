from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Roles"

class Empleado(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)
    email = models.EmailField(max_length=100, unique=True, blank=True, null=True)
    usuario = models.CharField(max_length=50, unique=True, blank=True, null=True)
    contraseña = models.CharField(max_length=255, blank=True, null=True)
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)
    email = models.EmailField(max_length=100, unique=True, blank=True, null=True)
    direccion = models.CharField(max_length=255)
    usuario = models.CharField(max_length=50, unique=True)
    contraseña = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10)
    direccion = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Proveedores"

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre

class Articulo(models.Model):
    codigo_sku = models.CharField(max_length=30, unique=True, blank=True, null=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    imagen_url = models.ImageField(upload_to='articulos/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('procesado', 'Procesado'),
        ('cancelado', 'Cancelado'),
    ]
    
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    
    def __str__(self):
        if self.id_cliente:
            return f"Carrito {self.id} - {self.id_cliente}"
        elif self.id_empleado:
            return f"Carrito {self.id} - {self.id_empleado} (Empleado)"
        return f"Carrito {self.id}"
    
    def get_total(self):
        total = sum(item.subtotal() for item in self.carritoitem_set.all())
        return total
    
    def get_owner_name(self):
        if self.id_cliente:
            return f"{self.id_cliente.nombre} {self.id_cliente.apellido}"
        elif self.id_empleado:
            return f"{self.id_empleado.nombre} {self.id_empleado.apellido} (Empleado)"
        return "Usuario Desconocido"
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(id_cliente__isnull=False, id_empleado__isnull=True) |
                    models.Q(id_cliente__isnull=True, id_empleado__isnull=False)
                ),
                name='carrito_owner_check'
            )
        ]

class CarritoItem(models.Model):
    id_carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    id_articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    
    class Meta:
        unique_together = ['id_carrito', 'id_articulo']
    
    def subtotal(self):
        return self.cantidad * self.id_articulo.precio
    
    def get_subtotal(self):
        return self.subtotal()

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='pedidos_procesados')
    id_comprador_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=True, blank=True, related_name='pedidos_comprados')
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    metodo_pago = models.CharField(max_length=50, blank=True, null=True)
    direccion_envio = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        if self.id_cliente:
            return f"Pedido #{self.id} - {self.id_cliente}"
        elif self.id_comprador_empleado:
            return f"Pedido #{self.id} - {self.id_comprador_empleado} (Empleado)"
        return f"Pedido #{self.id}"
    
    def get_cliente_name(self):
        if self.id_cliente:
            return f"{self.id_cliente.nombre} {self.id_cliente.apellido}"
        elif self.id_comprador_empleado:
            return f"{self.id_comprador_empleado.nombre} {self.id_comprador_empleado.apellido} (Empleado)"
        return "Cliente Desconocido"

class PedidoDetalle(models.Model):
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    id_articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    def subtotal(self):
        return self.cantidad * self.precio_unitario
    
    def get_subtotal(self):
        return self.subtotal()

class MovimientoInventario(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]
    
    id_articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.tipo.title()} - {self.id_articulo.nombre} ({self.cantidad})"

class Pago(models.Model):
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    metodo_pago = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"Pago #{self.id} - Pedido #{self.id_pedido.id}"