set search_path to bd1k;

-- Tabla Persona
CREATE TABLE Persona (
    DNI VARCHAR(8) PRIMARY KEY NOT NULL,
    nombre_completo VARCHAR(50) NOT NULL,
    edad INT NOT NULL
);

-- Tabla Trabajador
CREATE TABLE Trabajador (
    Persona_DNI VARCHAR(8) PRIMARY KEY NOT NULL,
    correo VARCHAR(50) NOT NULL,
    FOREIGN KEY (Persona_DNI) REFERENCES Persona(DNI)
);

-- Tabla Cliente
CREATE TABLE Cliente (
    Persona_DNI VARCHAR(8) PRIMARY KEY NOT NULL,
    celular VARCHAR(9) NOT NULL,
    FOREIGN KEY (Persona_DNI) REFERENCES Persona(DNI)
);

-- Tabla Empresa
CREATE TABLE Empresa (
    RUC VARCHAR(11) PRIMARY KEY NOT NULL,
    nombre VARCHAR(80) NOT NULL,
    direccion VARCHAR(300) NOT NULL,
    telefono VARCHAR(9) NOT NULL CHECK (telefono ~ '^9'),
    tipo VARCHAR(50) NOT NULL
);

-- Tabla Repartidor
CREATE TABLE Repartidor (
    Persona_DNI VARCHAR(8) PRIMARY KEY NOT NULL,
    calificacion SMALLINT NOT NULL CHECK (calificacion >= 1 AND calificacion <= 5),
    celular VARCHAR(9) NOT NULL,
    placa_vehiculo VARCHAR(7) NOT NULL,
    Courier_RUC VARCHAR(11) NOT NULL,
    FOREIGN KEY (Persona_DNI) REFERENCES Persona(DNI),
    FOREIGN KEY (Courier_RUC) REFERENCES Empresa(RUC)
);


-- Tabla Comercial
CREATE TABLE Comercial (
    Empresa_RUC VARCHAR(11) PRIMARY KEY NOT NULL,
    FOREIGN KEY (Empresa_RUC) REFERENCES Empresa(RUC)
);

-- Tabla Courier
CREATE TABLE Courier (
    Empresa_RUC VARCHAR(11) PRIMARY KEY NOT NULL,
    FOREIGN KEY (Empresa_RUC) REFERENCES Empresa(RUC)
);

-- Tabla Despacho
CREATE TABLE Despacho (
    direccion VARCHAR(200) PRIMARY KEY NOT NULL,
    nro_telefono VARCHAR(9) NOT NULL CHECK (nro_telefono ~ '^9')
);

-- Tabla Producto
CREATE TABLE Producto (
    modelo VARCHAR(15) NOT NULL,
    codigo VARCHAR(6) NOT NULL,
    precio FLOAT NOT NULL CHECK (precio > 0),
    descripcion TEXT NOT NULL,
    PRIMARY KEY (modelo, codigo)
);

-- Tabla Stock
CREATE TABLE Stock (
    Producto_modelo VARCHAR(15) NOT NULL,
    Producto_codigo VARCHAR(6) NOT NULL,
    Despacho_direccion VARCHAR(200) NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    PRIMARY KEY (Producto_modelo, Producto_codigo, Despacho_direccion),
    FOREIGN KEY (Producto_modelo, Producto_codigo) REFERENCES Producto(modelo, codigo),
    FOREIGN KEY (Despacho_direccion) REFERENCES Despacho(direccion)
);

-- Tabla Orden de compra
CREATE TABLE Orden_de_compra (
    codigo INT PRIMARY KEY NOT NULL,
    Empresa_RUC VARCHAR(11) NOT NULL,
    Despacho_direccion VARCHAR(200) NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (Empresa_RUC) REFERENCES Empresa(RUC),
    FOREIGN KEY (Despacho_direccion) REFERENCES Despacho(direccion)
);

-- Tabla Abastecimiento
CREATE TABLE Abastecimiento (
    Orden_de_compra_codigo INT NOT NULL,
    Producto_modelo VARCHAR(15) NOT NULL,
    Producto_codigo VARCHAR(6) NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    PRIMARY KEY (Orden_de_compra_codigo, Producto_modelo, Producto_codigo),
    FOREIGN KEY (Orden_de_compra_codigo) REFERENCES Orden_de_compra(codigo),
    FOREIGN KEY (Producto_modelo, Producto_codigo) REFERENCES Producto(modelo, codigo)
);

-- Tabla Comprobante de pago
CREATE TABLE Comprobante_de_pago (
    codigo INT PRIMARY KEY NOT NULL
);

-- Tabla Venta
CREATE TABLE Venta (
    codigo INT PRIMARY KEY NOT NULL,
    Comprobante_de_pago_codigo INT NOT NULL,
    fecha TIMESTAMP NOT NULL,
    total FLOAT NOT NULL,
    costo_envio FLOAT NOT NULL CHECK (costo_envio > 0),
    fecha_y_hora_envio TIMESTAMP NOT NULL,
    estado VARCHAR(10) NOT NULL,
    direccion_destino VARCHAR(200) NOT NULL,
    Repartidor_DNI VARCHAR(8) NOT NULL,
    es_virtual BOOLEAN NOT NULL,
    Persona_DNI VARCHAR(8) NOT NULL,
    FOREIGN KEY (Comprobante_de_pago_codigo) REFERENCES Comprobante_de_pago(codigo),
    FOREIGN KEY (Repartidor_DNI) REFERENCES Repartidor(Persona_DNI),
    FOREIGN KEY (Persona_DNI) REFERENCES Persona(DNI)
);

-- Tabla Pago
CREATE TABLE Pago (
    Venta_codigo INT NOT NULL,
    metodo_pago VARCHAR(15) NOT NULL CHECK (metodo_pago IN ('Yape', 'Plin', 'Visa', 'MasterCard', 'Efectivo')),
    Trabajador_DNI VARCHAR(8) NOT NULL,
    monto FLOAT NOT NULL CHECK (monto > 0),
    PRIMARY KEY (Venta_codigo, metodo_pago),
    FOREIGN KEY (Venta_codigo) REFERENCES Venta(codigo),
    FOREIGN KEY (Trabajador_DNI) REFERENCES Trabajador(Persona_DNI)
);


-- Tabla Item vendido
CREATE TABLE Item_vendido (
    Producto_modelo VARCHAR(15) NOT NULL,
    Producto_codigo VARCHAR(6) NOT NULL,
    Venta_codigo INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    subtotal FLOAT NOT NULL,
    PRIMARY KEY (Producto_modelo, Producto_codigo, Venta_codigo),
    FOREIGN KEY (Producto_modelo, Producto_codigo) REFERENCES Producto(modelo, codigo),
    FOREIGN KEY (Venta_codigo) REFERENCES Venta(codigo)
);
