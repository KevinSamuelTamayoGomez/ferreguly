CREATE DATABASE IF NOT EXISTS ferreguly;
USE ferreguly;

DROP TABLE IF EXISTS pago;
DROP TABLE IF EXISTS movimiento_inventario;
DROP TABLE IF EXISTS pedido_detalle;
DROP TABLE IF EXISTS pedido;
DROP TABLE IF EXISTS carrito_item;
DROP TABLE IF EXISTS carrito;
DROP TABLE IF EXISTS articulo;
DROP TABLE IF EXISTS categoria;
DROP TABLE IF EXISTS proveedor;
DROP TABLE IF EXISTS cliente;
DROP TABLE IF EXISTS empleado;
DROP TABLE IF EXISTS rol;

CREATE TABLE rol (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion VARCHAR(255)
);

CREATE TABLE empleado (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    cargo VARCHAR(50) NOT NULL,
    telefono VARCHAR(10) NOT NULL,
    email VARCHAR(100) UNIQUE,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    id_rol INT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_rol) REFERENCES rol(id)
);

CREATE TABLE cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    telefono VARCHAR(10) NOT NULL,
    email VARCHAR(100) UNIQUE,
    direccion VARCHAR(255) NOT NULL,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE proveedor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(10) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE categoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT
);

CREATE TABLE articulo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo_sku VARCHAR(30) UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    precio DECIMAL(10,2) NOT NULL CHECK (precio > 0),
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
    id_categoria INT NOT NULL,
    id_proveedor INT NOT NULL,
    imagen_url VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id),
    FOREIGN KEY (id_proveedor) REFERENCES proveedor(id)
);

CREATE TABLE carrito (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NULL,
    id_empleado INT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('activo','procesado','cancelado') DEFAULT 'activo',
    FOREIGN KEY (id_cliente) REFERENCES cliente(id),
    FOREIGN KEY (id_empleado) REFERENCES empleado(id),
    CHECK ((id_cliente IS NOT NULL AND id_empleado IS NULL) OR (id_cliente IS NULL AND id_empleado IS NOT NULL))
);

CREATE TABLE carrito_item (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_carrito INT NOT NULL,
    id_articulo INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    FOREIGN KEY (id_carrito) REFERENCES carrito(id) ON DELETE CASCADE,
    FOREIGN KEY (id_articulo) REFERENCES articulo(id) ON DELETE CASCADE,
    UNIQUE KEY (id_carrito, id_articulo)
);

CREATE TABLE pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NULL,
    id_empleado INT NOT NULL,
    id_comprador_empleado INT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('pendiente', 'completado', 'cancelado') DEFAULT 'pendiente',
    total DECIMAL(10,2) NOT NULL DEFAULT 0,
    metodo_pago VARCHAR(50),
    direccion_envio VARCHAR(255),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id),
    FOREIGN KEY (id_empleado) REFERENCES empleado(id),
    FOREIGN KEY (id_comprador_empleado) REFERENCES empleado(id)
);

CREATE TABLE pedido_detalle (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_articulo INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES pedido(id) ON DELETE CASCADE,
    FOREIGN KEY (id_articulo) REFERENCES articulo(id)
);

CREATE TABLE movimiento_inventario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_articulo INT NOT NULL,
    id_empleado INT NOT NULL,
    tipo ENUM('entrada','salida') NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    descripcion VARCHAR(255),
    FOREIGN KEY (id_articulo) REFERENCES articulo(id),
    FOREIGN KEY (id_empleado) REFERENCES empleado(id)
);

CREATE TABLE pago (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_empleado INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    monto DECIMAL(10,2) NOT NULL CHECK (monto > 0),
    metodo_pago VARCHAR(50),
    FOREIGN KEY (id_pedido) REFERENCES pedido(id),
    FOREIGN KEY (id_empleado) REFERENCES empleado(id)
);

CREATE INDEX idx_cliente_usuario ON cliente(usuario);
CREATE INDEX idx_empleado_usuario ON empleado(usuario);
CREATE INDEX idx_carrito_estado ON carrito(estado);
CREATE INDEX idx_carrito_cliente ON carrito(id_cliente);
CREATE INDEX idx_carrito_empleado ON carrito(id_empleado);
CREATE INDEX idx_pedido_cliente ON pedido(id_cliente);
CREATE INDEX idx_pedido_empleado ON pedido(id_empleado);
CREATE INDEX idx_pedido_comprador_empleado ON pedido(id_comprador_empleado);
CREATE INDEX idx_pedido_fecha ON pedido(fecha);
CREATE INDEX idx_movimiento_fecha ON movimiento_inventario(fecha);
CREATE INDEX idx_articulo_activo ON articulo(activo);
CREATE INDEX idx_articulo_stock ON articulo(stock);


INSERT INTO rol (nombre, descripcion) VALUES 
('Administrador', 'Acceso completo al sistema'),
('Gerente General', 'Gestión general de la ferretería'),
('Jefe de Ventas', 'Supervisión del área de ventas'),
('Vendedor', 'Atención al cliente y ventas'),
('Almacenista', 'Gestión de inventario y almacén'),
('Cajero', 'Manejo de pagos');

INSERT INTO empleado (nombre, apellido, cargo, telefono, email, usuario, contraseña, id_rol) VALUES 
('Carlos', 'Admin', 'Administrador', '9611111111', 'admin@ferreguly.com', 'admin', 'admin123', 1),
('Roberto Carlos', 'Hernández Mendoza', 'Gerente General', '9611234567', 'roberto.hernandez@ferreguly.com', 'rhernandez', 'Gerente2024', 2),
('José Luis', 'Martínez Cruz', 'Jefe de Ventas', '9613456789', 'jose.martinez@ferreguly.com', 'jmartinez', 'Ventas2024', 3),
('María Elena', 'Gómez Vásquez', 'Administradora', '9612345678', 'maria.gomez@ferreguly.com', 'mgomez', 'Admin2024', 1),
('Ana', 'Ventas', 'Vendedora', '9612222222', 'ana@ferreguly.com', 'ana_vendedor', 'venta123', 4),
('Luis', 'Almacén', 'Almacenista', '9613333333', 'luis@ferreguly.com', 'luis_almacen', 'almacen123', 5);

INSERT INTO cliente (nombre, apellido, telefono, email, direccion, usuario, contraseña) VALUES 
('Juan', 'Pérez', '9614444444', 'juan@email.com', 'Calle Principal #123', 'juan_cliente', 'juan123'),
('María', 'García', '9615555555', 'maria@email.com', 'Av. Central #456', 'maria_cliente', 'maria123'),
('Pedro', 'López', '9616666666', 'pedro@email.com', 'Col. Centro #789', 'pedro_cliente', 'pedro123'),
('Samuel', 'Gomez', '9612627700', 'kevin.samuel.gomez@outlook.com', 'calle la gloria 575', 'samuel_cliente', 'samuel123'),
('Cliente', 'Prueba', '9611111111', 'cliente@test.com', 'Calle de Prueba #123', 'cliente_test', 'test123');

INSERT INTO proveedor (nombre, telefono, direccion) VALUES 
('Grupo Kuo (Desc)', '5550818000', 'Blvd. Manuel Ávila Camacho 36, Lomas de Chapultepec, CDMX'),
('CEMEX', '5550008000', 'Av. Ricardo Margáin Zozaya 325, Santa Engracia, San Pedro Garza García, N.L.'),
('Truper', '5553121000', 'Parque Industrial Jilotepec, Estado de México'),
('DeWalt México (Stanley Black & Decker)', '5591774900', 'Periferico Sur 7980, Tlalpan, CDMX'),
('Bosch México', '5554821000', 'Av. Robert Bosch 2000, Toluca, Estado de México'),
('Condumex (Grupo Carso)', '5511034000', 'Av. Juan Salvador Agraz 69, Santa Fe, CDMX'),
('Rotoplas', '5552015000', 'Av. Constituyentes 1055, Miguel Hidalgo, CDMX'),
('Comex (PPG Comex)', '5552794444', 'Av. Tamaulipas 141, Hipódromo Condesa, CDMX'),
('Sherwin Williams México', '5550810600', 'Blvd. Manuel Ávila Camacho 36, Miguel Hidalgo, CDMX'),
('Urrea Herramientas', '4433190090', 'Carretera a Zapotlanejo Km 7.5, Tonalá, Jalisco'),
('Pretul (Grupo Bellota)', '3337709400', 'Av. Washington 1515, Guadalajara, Jalisco'),
('Surtek', '8186254600', 'Av. Universidad 1738, Monterrey, N.L.'),
('Plastigama México', '5558047500', 'Anillo Periférico 3332, Guadalajara, Jalisco'),
('Volteck', '3336662200', 'Calle 8 #730, Zona Industrial, Guadalajara, Jalisco'),
('3M México', '5552700400', 'Av. Santa Fe 495, Santa Fe, CDMX');

INSERT INTO categoria (nombre, descripcion) VALUES 
('Herramientas Manuales', 'Martillos, desarmadores, llaves, alicates, sierras manuales, cinceles, limas, escuadras y herramientas de mano en general.'),
('Herramientas Eléctricas', 'Taladros, sierras eléctricas, lijadoras, esmeriles, rotomartillos, pulidoras y herramientas con motor eléctrico.'),
('Materiales de Construcción', 'Cemento, cal, yeso, mortero, blocks, tabiques, varillas, alambrón, malla electrosoldada y materiales básicos de construcción.'),
('Plomería', 'Tuberías de PVC, cobre y galvanizadas, conexiones, llaves de agua, válvulas, medidores, bombas y accesorios hidráulicos.'),
('Electricidad', 'Cables, conductores, interruptores, contactos, centros de carga, breakers, luminarias y material eléctrico en general.'),
('Pinturas y Acabados', 'Pinturas vinílicas, esmaltes, impermeabilizantes, barnices, selladores, brochas, rodillos y accesorios para pintura.'),
('Tornillería y Fijaciones', 'Tornillos, tuercas, arandelas, clavos, taquetes, anclas, remaches y elementos de fijación diversos.'),
('Ferretería General', 'Candados, cerraduras, bisagras, herrajes, cadenas, cables de acero, poleas y accesorios metálicos diversos.'),
('Jardín y Exteriores', 'Mangueras, aspersores, herramientas de jardín, macetas, fertilizantes y productos para áreas verdes.'),
('Seguridad Industrial', 'Cascos, guantes, lentes de seguridad, arneses, botas industriales y equipo de protección personal.');

-- ===============================================
-- DATOS DE ARTÍCULOS
-- ===============================================
INSERT INTO articulo (codigo_sku, nombre, descripcion, precio, stock, id_categoria, id_proveedor, imagen_url) VALUES 
-- Herramientas Manuales
('TRU-MAR-16', 'Martillo de Uña 16 oz Truper Mango Fibra', 'Martillo de uña con cabeza de acero al carbón forjado, mango de fibra de vidrio con grip antideslizante. Peso balanceado para mayor precisión. Incluye garantía del fabricante.', 185.50, 25, 1, 3, 'articulos/martillo-16-oz-u-a-recta-mango-fibra-de-vidrio-truper-c9f.jpg'),
('TRU-DES-8P', 'Juego de Desarmadores 8 Piezas Truper', 'Set de 8 desarmadores con puntas plana y phillips. Mangos ergonómicos con grip antideslizante. Incluye medidas: 3/16, 1/4, 5/16, 3/8 planas y #0, #1, #2, #3 phillips.', 125.00, 40, 1, 3, 'articulos/imagen_2025-05-30_010934670.png'),
('TRU-LLI-12', 'Llave Inglesa 12" Truper Acero Forjado', 'Llave inglesa de 12 pulgadas fabricada en acero forjado con acabado cromado. Mordazas paralelas, graduación clara. Apertura máxima 35mm.', 145.75, 30, 1, 3, 'articulos/imagen_2025-05-30_013520610.png'),

-- Herramientas Eléctricas
('DWT-D25133K', 'Rotomartillo SDS Plus 800W DeWalt D25133K', 'Rotomartillo electroneumático de 800W con sistema SDS Plus. 3 modos de operación: taladrado, taladrado con percusión y cincelado. Incluye maletín y cincel plano.', 4250.00, 8, 2, 4, 'articulos/imagen_2025-05-30_013624497.png'),
('DWT-DCD771D2', 'Taladro Atornillador 20V DeWalt DCD771D2', 'Taladro inalámbrico de 20V con 2 baterías de litio de 2.0Ah. Mandril de 13mm, 15 posiciones de torque, luz LED, cargador rápido y estuche.', 3850.00, 12, 2, 4, 'articulos/imagen_2025-05-30_013731145.png'),
('BSH-GKS190', 'Sierra Circular 7 1/4" Bosch GKS 190', 'Sierra circular de mano de 1400W con disco de 7 1/4". Sistema de protección, guía paralela, profundidad de corte 70mm a 90°. Motor potente y duradero.', 2950.00, 15, 2, 5, 'articulos/imagen_2025-05-30_013917158.png'),

-- Materiales de Construcción
('CMX-CEM-50', 'Cemento Portland Gris CEMEX 50kg', 'Cemento Portland Compuesto gris, saco de 50kg. Cumple norma NMX-C-414-ONNCCE. Ideal para obras generales, cimentaciones, columnas y elementos estructurales.', 185.00, 100, 3, 2, 'articulos/imagen_2025-05-30_014150827.png'),
('CMX-VAR-38', 'Varilla Corrugada 3/8" x 12m', 'Varilla corrugada de acero grado 42, diámetro 3/8" (9.5mm) x 12 metros. Cumple normas mexicanas, ideal para refuerzo de concreto en construcción.', 85.50, 200, 3, 2, 'articulos/imagen_2025-05-30_014320811.png'),

-- Plomería
('ROT-PVC-4', 'Tubo PVC Sanitario 4" x 6m Rotoplas', 'Tubo PVC sanitario serie inglesa de 4" x 6m, color naranja, campana integrada. Cumple norma NMX-E-215-CNCP. Para desagües y drenajes.', 265.00, 50, 4, 7, 'articulos/imagen_2025-05-30_014441840.png'),
('ROT-TIN-1100', 'Tinaco Rotoplas 1100L Tricapa', 'Tinaco de polietileno tricapa de 1100 litros. Sistema Hydro-Net, tapa click, flotador y accesorios incluidos. Garantía de 5 años.', 4850.00, 20, 4, 7, 'articulos/imagen_2025-05-30_014540931.png'),

-- Electricidad
('CDX-THW-12', 'Cable THW 12 AWG Condumex 100m', 'Cable conductor de cobre suave THW calibre 12 AWG, rollo de 100m. Aislamiento de PVC, 90°C. Para instalaciones eléctricas residenciales.', 1650.00, 25, 5, 6, 'articulos/imagen_2025-05-30_014625714.png'),
('VLT-CC-8', 'Centro de Carga 8 Polos Volteck', 'Centro de carga monofásico de 8 polos, 120/240V. Incluye interruptor principal de 100A, barra de neutros y tierra. Gabinete metálico NEMA 1.', 850.00, 15, 5, 14, 'articulos/imagen_2025-05-30_014840988.png'),

-- Pinturas y Acabados
('CMX-VIN-4L', 'Vinimex Blanco Mate Comex 4L', 'Pintura vinílica lavable de alta calidad, acabado mate. Rendimiento: 40-45 m²/cubeta. Secado rápido, excelente cubrimiento. Para interiores.', 485.00, 35, 6, 8, 'articulos/imagen_2025-05-30_015046841.png'),
('CMX-IMP-19L', 'Impermeabilizante Rojo Ladrillo Comex 19L', 'Impermeabilizante acrílico de máxima calidad, color rojo ladrillo. Resistente a la intemperie, flexible, fácil aplicación. Rendimiento: 3-4 m²/L.', 1850.00, 20, 6, 8, 'articulos/imagen_2025-05-30_015230779.png'),

-- Ferretería General
('TRU-CAN-50', 'Candado de Latón 50mm Truper', 'Candado con cuerpo de latón sólido de 50mm, arco de acero templado. Mecanismo de 5 pines, resistente a la corrosión. Incluye 3 llaves.', 125.00, 60, 8, 3, 'articulos/imagen_2025-05-30_015439413.png'),
('TRU-CAD-1/4', 'Cadena Galvanizada 1/4" x 10m Truper', 'Cadena de acero galvanizado de 1/4" por rollo de 10 metros. Eslabones soldados, resistente a la oxidación. Para uso general y amarre.', 385.00, 25, 8, 3, 'articulos/imagen_2025-05-30_015534808.png'),

-- Seguridad Industrial
('3M-CSC-H700', 'Casco de Seguridad Blanco H-700 3M', 'Casco industrial de polietileno de alta densidad, suspensión tipo trinquete. Cumple normas ANSI Z89.1. Resistente al impacto y penetración.', 285.00, 40, 10, 15, 'articulos/imagen_2025-05-30_015721887.png'),
('3M-GUA-CUT5', 'Guantes Cut Level 5 3M Comfort Grip', 'Guantes de alta resistencia al corte nivel 5, recubrimiento de nitrilo. Ajuste cómodo, destreza táctil. Talla M, L, XL disponibles.', 165.00, 80, 10, 15, 'articulos/imagen_2025-05-30_015853594.png');

