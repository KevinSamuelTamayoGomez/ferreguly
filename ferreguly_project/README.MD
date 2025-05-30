# 🔧 Ferreguly - Sistema de Ferretería

Sistema web completo para gestión de ferretería desarrollado con Django. Incluye sistema de login dual para clientes y empleados, gestión de inventario, pedidos y roles administrativos.

## 🚀 Características Principales

### 🔐 Sistema de Autenticación Dual
- **Clientes**: Registro público, compras, historial de pedidos
- **Empleados**: Sistema administrativo con roles específicos
- **Login Unificado**: Detección automática del tipo de usuario

### 🛒 E-Commerce
- Catálogo público de productos
- Carrito de compras (requiere login)
- Proceso de checkout completo
- Múltiples métodos de pago

### 👥 Gestión de Usuarios y Roles
- **Administrador**: Acceso completo al sistema
- **Gerente General**: Gestión general de la ferretería
- **Jefe de Ventas**: Supervisión del área de ventas
- **Vendedor**: Atención al cliente y ventas
- **Almacenista**: Gestión de inventario y almacén

### 📦 Gestión de Inventario
- Control de stock en tiempo real
- Movimientos de entrada y salida
- Historial completo de movimientos
- Alertas de stock bajo

### 📊 Gestión Administrativa
- CRUD completo de productos, categorías, proveedores
- Gestión de pedidos y estados
- Reportes de movimientos
- Dashboard administrativo

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 4.2+
- **Base de Datos**: SQLite3
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Imágenes**: Pillow para manejo de archivos
- **Iconos**: Bootstrap Icons

## 📋 Requisitos del Sistema

- Python 3.8+
- Django 4.2+
- Pillow 10.0+
- SQLite3 (incluido con Python)

## ⚡ Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone https://github.com/KevinSamuelTamayoGomez/ferreguly.git
cd ferreguly
```

### 2. Crear Entorno Virtual
```bash
python -m venv ferreguly_venv
```

### 3. Activar Entorno Virtual
**Windows:**
```bash
ferreguly_venv\Scripts\activate
```

**macOS/Linux:**
```bash
source ferreguly_venv/bin/activate
```

### 4. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar Base de Datos
```bash
python manage.py makemigrations ferreguly
python manage.py migrate
```

### 6. Cargar Datos de Prueba (Opcional)
```bash
# Ejecutar el SQL proporcionado en database/ferreguly_complete.sql
# O crear datos manualmente desde el admin de Django
```

### 7. Crear Superusuario (Opcional)
```bash
python manage.py createsuperuser
```

### 8. Ejecutar el Servidor
```bash
python manage.py runserver
```

Visita `http://127.0.0.1:8000` para acceder al sistema.

## 👤 Usuarios de Prueba

### Empleados
| Usuario | Contraseña | Rol |

|---------|------------|-----|
| `mgomez` | `Admin2024` | Administrador |
| `rhernandez` | `Gerente2024` | Gerente General |
| `jmartinez` | `Ventas2024` | Jefe de Ventas |

### Clientes
Puedes registrar nuevos clientes desde la página de registro público, o usar:
| Usuario | Contraseña |
|---------|------------|
| `cliente_test` | `test123` |

## 📁 Estructura del Proyecto

```
ferreguly/
├── ferreguly_project/          # Configuración principal de Django
├── ferreguly/                  # Aplicación principal
│   ├── models.py              # Modelos de datos
│   ├── views.py               # Lógica de vistas
│   ├── forms.py               # Formularios
│   ├── urls.py                # URLs de la aplicación
│   ├── decorators.py          # Decoradores de autenticación
│   └── templates/             # Templates HTML
│       └── ferreteria/
├── static/                    # Archivos estáticos
├── media/                     # Archivos subidos por usuarios
├── requirements.txt           # Dependencias del proyecto
└── README.md                 # Este archivo
```

## 🔒 Sistema de Permisos

### Acceso Público (Sin Login)
- ✅ Ver catálogo de productos
- ✅ Información general
- ❌ Agregar al carrito (requiere login)

### Clientes Registrados
- ✅ Comprar productos
- ✅ Ver historial de pedidos
- ✅ Gestionar perfil personal
- ❌ Acceso administrativo

### Empleados por Rol

#### 🔴 Administrador
- ✅ Acceso completo al sistema
- ✅ Gestionar empleados y roles
- ✅ Eliminar cualquier registro

#### 🟠 Almacenista
- ✅ Gestionar inventario
- ✅ Movimientos de stock
- ✅ Proveedores y categorías
- ❌ Gestionar empleados

#### 🟡 Vendedor/Jefe de Ventas
- ✅ Gestionar clientes
- ✅ Procesar pedidos
- ✅ Ver historial de ventas
- ❌ Gestionar inventario

## 🌟 Funcionalidades Destacadas

### 🛒 Carrito Inteligente
- Validación de stock en tiempo real
- Soporte para clientes y empleados
- Persistencia de sesión

### 📈 Control de Inventario
- Actualizaciones automáticas de stock
- Trazabilidad completa de movimientos
- Reportes detallados

### 🔄 Sistema de Pedidos
- Estados: Pendiente, Completado, Cancelado
- Reversión automática de stock en cancelaciones
- Múltiples métodos de pago

### 🎨 Interfaz de Usuario
- Diseño responsive con Bootstrap 5
- Navegación intuitiva
- Indicadores visuales de estado
- Mensajes informativos

## 🐛 Solución de Problemas Comunes

### Error de Migración
```bash
python manage.py makemigrations --empty ferreguly
python manage.py migrate
```

### Error de Permisos de Login
```bash
python manage.py shell
from ferreguly.models import Empleado, Rol
# Crear usuario admin manualmente
```

### Error de Archivos Estáticos
```bash
python manage.py collectstatic
```

## 📞 Contacto

- **Desarrollador**: Kevin Samuel Tamayo Gómez
- **Email**: kevin.samuel.gomez@outlook.com
- **Proyecto**: Sistema de Ferretería Ferreguly

## 🎯 Próximas Funcionalidades

- [ ] Dashboard con estadísticas
- [ ] Reportes en PDF
- [ ] Notificaciones por email
- [ ] API REST
- [ ] Aplicación móvil
- [ ] Integración con sistemas de pago

---

⭐ Si te gusta este proyecto, ¡dale una estrella en GitHub!

🚀 **Ferreguly** - Tu ferretería digital completa en Django.