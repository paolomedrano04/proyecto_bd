import psycopg2
import random
from datetime import timedelta, datetime
import string
from faker import Faker

# Conectar a la base de datos
conn = psycopg2.connect(
    database="bdmil",
    user="postgres",
    password="ut3c1719",
    host="localhost",
    port="5432",
    options="-c search_path=bdpruebas"
)
cursor = conn.cursor()

conn.autocommit = True

# Crear una instancia de Faker
fake = Faker()

# Lista fija de productos
productos_fijos = [
    #Medallas
    ('Medalla', 'M001', 17.00, 'Aleación de metales Zamak 2.1cm'), 
    ('Medalla', 'M002', 12.00, 'Aleación de metales Zamak 1.5cm'),
    ('Medalla', 'M003', 13.00, 'Aleación de metales Zamak 2.2cm'),
    ('Medalla', 'M004', 12.00, 'Aleación de metales Zamak 2.8cm'),
    ('Medalla', 'M005', 60.00, 'Medalla de San Benito plata 950'),
    ('Medalla', 'M006', 45.00, 'Medalla de San Benito plata 950 1.7cm'), 
    ('Medalla', 'M007', 30.00, 'Medalla de San Benito plata 950 1.4cm'), 
    ('Medalla', 'M008', 54.00, 'Medalla de San Benito plata 950 1.8cm'),
    ('Medalla', 'M009', 35.00, 'Medalla Corazon de Jesus'), 
    ('Medalla', 'M010', 40.00, 'Medalla Virgen de Guadalupe'), 
    ('Medalla', 'M011', 40.00, 'Medalla de San Miguel Arcángel'), 
    ('Medalla', 'M012', 40.00, 'Medalla de Divino Nino'), 
    ('Medalla', 'M013', 45.00, 'Medalla de Señor de los Milagros'),
    ('Medalla', 'M014', 28.00, 'Medalla de Señor de Luren'), 
    ('Medalla', 'M015', 45.00, 'Medalla de Padre Pio'), 
    ('Medalla', 'M016', 20.00, 'Medalla Milagrosa'),
    ('Medalla', 'M017', 70.00, 'Medalla nacar San Benito'),
    ('Medalla', 'M018', 28.00, 'Medalla llave San Benito'), 
    ('Medalla', 'M019', 16.00, 'Medalla de Santa Rosa de Lima'),
    ('Medalla', 'M020', 17.00, 'Medalla de San Pedro'), 

    # Medallones 
    ('Medallón', 'P001', 10.00, 'Medallón de la Virgen de Guadalupe'),
    ('Medallón', 'P002', 9.50, 'Medallón de San Judas Tadeo'), 
    ('Medallón', 'P003', 10.20, 'Medallón de San Benito'), 
    ('Medallón', 'P004', 9.80, 'Medallón del Sagrado Corazón'), 
    ('Medallón', 'P005', 10.40, 'Medallón del Santo Rosario'),
    ('Medallón', 'P006', 9.60, 'Medallón de la Milagrosa'),
    ('Medallón', 'P007', 10.30, 'Medallón de San Miguel Arcángel'), 
    ('Medallón', 'P008', 9.70, 'Medallón de San Rafael Arcángel'),
    ('Medallón', 'P009', 10.10, 'Medallón de San Gabriel Arcángel'), 
    ('Medallón', 'P010', 9.90, 'Medallón de San Antonio de Padua'),

    # Imagenes
    ('Imagen', 'I001', 40.00, 'Imagen de San Miguel 13cm'), 
    ('Imagen', 'I002', 40.00, 'Imagen de Rosa Mistica 13cm'),
    ('Imagen', 'I003', 40.00, 'Imagen de Medalla Milagrosa 13cm'),
    ('Imagen', 'I004', 40.00, 'Imagen de Virgen del Carmen 13cm'), 
    ('Imagen', 'I005', 65.00, 'Imagen de Medalla Milagrosa 20cm'), 
    ('Imagen', 'I006', 65.00, 'Imagen de Virgen Desatanudos 20cm'), 
    ('Imagen', 'I007', 65.00, 'Imagen de Rosa Mistica 20cm'), 
    ('Imagen', 'I008', 65.00, 'Imagen de Maria Auxiliadora 20cm'), 
    ('Imagen', 'I009', 65.00, 'Imagen de Virgen Maria'),
    ('Imagen', 'I010', 65.00, 'Imagen de Corazon de Maria'), 
    ('Imagen', 'I011', 65.00, 'Imagen de Virgen del Carmen rosada'), 
    ('Imagen', 'I012', 65.00, 'Imagen de Virgen de Guadalupe'), 
    ('Imagen', 'I013', 65.00, 'Imagen de Virgen de Fatima'), 
    ('Imagen', 'I014', 65.00, 'Imagen de Dulce Espera'),
    ('Imagen', 'I015', 65.00, 'Imagen de San Jose'), 
    ('Imagen', 'I016', 65.00, 'Imagen de San Jose dormido'), 
    ('Imagen', 'I017', 65.00, 'Imagen de San Francisco Javier'), 
    ('Imagen', 'I018', 65.00, 'Imagen de San Miguel Arcangel'),
    ('Imagen', 'I019', 65.00, 'Imagen de San Rafael'), 
    ('Imagen', 'I020', 65.00, 'Imagen de San Gabriel'),
    ('Imagen', 'I021', 65.00, 'Imagen de San Martin'),
    ('Imagen', 'I022', 75.00, 'Imagen de Sagrada familia'),
    ('Imagen', 'I023', 60.00, 'Imagen de San Judas Tadeo'),
    ('Imagen', 'I024', 85.00, 'Imagen de Señor de los Milagros'),
    ('Imagen', 'I025', 65.00, 'Imagen de San Pio'),
    ('Imagen', 'I026', 65.00, 'Imagen de San Benito'),
    ('Imagen', 'I027', 65.00, 'Imagen de San Antonio'),
    ('Imagen', 'I028', 65.00, 'Imagen de Divina Misericordia'),

    # Cruces
    ('Cruz', 'CP01', 65.00, 'Cruz del perdón plata'), 
    ('Cruz', 'CP02', 75.00, 'Cruz del perdón oro'),
    ('Cruz', 'CP03', 45.00, 'Cruz de San Damián'),
    ('Cruz', 'CP04', 43.00, 'Cruz del Buen Pastor'),

    # Relicarios
    ('Relicario', 'R001', 12.00, 'Relicario de la Virgen María'),
    ('Relicario', 'R002', 11.50, 'Relicario de Jesús Cristo'),
    ('Relicario', 'R003', 12.20, 'Relicario de San José'),
    ('Relicario', 'R004', 11.80, 'Relicario de San Juan Bautista'),
    ('Relicario', 'R005', 12.40, 'Relicario de Santa Clara'),
    ('Relicario', 'R006', 11.60, 'Relicario de San Francisco de Asís'),
    ('Relicario', 'R007', 12.30, 'Relicario de Santa Teresa de Calcuta'),
    ('Relicario', 'R008', 11.70, 'Relicario de San Antonio de Padua'),
    ('Relicario', 'R009', 12.10, 'Relicario de Santa Rosa de Lima'),
    ('Relicario', 'R010', 11.90, 'Relicario de San Martín de Porres'),

    # Anillos
    ('Anillo', 'AS001', 15.00, 'Anillo con cruz de plata'),
    ('Anillo', 'AS002', 14.50, 'Anillo con imagen de la Virgen María'),
    ('Anillo', 'AS003', 15.20, 'Anillo de San Benito'),
    ('Anillo', 'AS004', 14.80, 'Anillo de San Judas Tadeo'),
    ('Anillo', 'AS005', 15.40, 'Anillo con el Padre Nuestro'),
    ('Anillo', 'AS006', 14.60, 'Anillo de San Francisco de Asís'),
    ('Anillo', 'AS007', 15.30, 'Anillo con imagen de Jesús Cristo'),
    ('Anillo', 'AS008', 14.70, 'Anillo con el Ave María'),
    ('Anillo', 'AS009', 15.10, 'Anillo de San Miguel Arcángel'),
    ('Anillo', 'AS010', 14.90, 'Anillo de San Gabriel Arcángel'),

    # Rosarios
    ('Rosario', 'RR001', 8.00, 'Rosario de madera de olivo'),
    ('Rosario', 'RR002', 7.50, 'Rosario de cuentas de cristal'),
    ('Rosario', 'RR003', 8.30, 'Rosario de perlas blancas'),
    ('Rosario', 'RR004', 7.70, 'Rosario de metal plateado'),
    ('Rosario', 'RR005', 8.20, 'Rosario de piedra volcánica'),
    ('Rosario', 'RR006', 7.80, 'Rosario de cuentas de madera'),
    ('Rosario', 'RR007', 8.40, 'Rosario de cuentas de vidrio'),
    ('Rosario', 'RR008', 7.60, 'Rosario de metal dorado'),
    ('Rosario', 'RR009', 8.10, 'Rosario de madera de nogal'),
    ('Rosario', 'RR010', 8.50, 'Rosario de perlas rosadas'),

    # Llaveros
    ('Llavero', 'L001', 14.00, 'Llavero con cruz de San Benito esmaltado'),
    ('Llavero', 'L002', 12.50, 'Llavero de la Virgen María'),
    ('Llavero', 'L003', 12.00, 'Llavero de Jesús Cristo'),
    ('Llavero', 'L004', 12.00, 'Llavero de San José'),
    ('Llavero', 'L005', 12.00, 'Llavero de San Francisco de Asís'),
    ('Llavero', 'L006', 13.00, 'Llavero de Santa Clara esmaltado'),
    ('Llavero', 'L007', 18.00, 'Llavero de Virgen con pompones'),
    ('Llavero', 'L008', 18.00, 'Llavero de San Benito con pompones'),
    ('Llavero', 'L009', 10.00, 'Llavero de Cruz'),
    ('Llavero', 'L010', 12.00, 'Llavero de Cruz esmaltado'),
    ('Llavero', 'L011', 14.00, 'Llavero con rosario'),
    ('Llavero', 'L012', 15.00, 'Llavero con sujetador'),

    # Recuerdos
    ('Recuerdo', 'RE001', 11.50, 'Recuerdo Porta aguabendita'),
    ('Recuerdo', 'RE002', 12.00, 'Recuerdo imantado'),
    ('Recuerdo', 'RE003', 12.00, 'Recuerdo de San José pedestal imantado'),
    ('Recuerdo', 'RE004', 12.00, 'Recuerdo de San Juan Bautista pedestal imantado'),
    ('Recuerdo', 'RE005', 11.50, 'Recuerdo de Santa Clara pedestal imantado'),
    ('Recuerdo', 'RE006', 11.50, 'Recuerdo de San Francisco de Asís pedestal imantado'),
    ('Recuerdo', 'RE007', 13.00, 'Recuerdo de Santa Teresa de Calcuta pedestal imantado'),
    ('Recuerdo', 'RE008', 10.00, 'Recuerdo de San Antonio de Padua'),
    ('Recuerdo', 'RE009', 10.00, 'Recuerdo de Santa Rosa de Lima'),
    ('Recuerdo', 'RE010', 10.50, 'Recuerdo de San Martín de Porres'),

    # Pulseras
    ('Pulsera', 'DP001', 38.00, 'Pulsera con medalla de San Benito'),
    ('Pulsera', 'DP002', 38.00, 'Pulsera con cruz de plata'),
    ('Pulsera', 'DP003', 38.00, 'Pulsera de cuentas de madera'),
    ('Pulsera', 'DP004', 34.00, 'Pulsera de cuentas de cristal'),
    ('Pulsera', 'DP005', 54.00, 'Pulsera de cuero con cruz'),
    ('Pulsera', 'DP006', 45.00, 'Pulsera de cuentas de vidrio'),
    ('Pulsera', 'DP007', 45.00, 'Pulsera con imagen de la Virgen de Guadalupe'), 
    ('Pulsera', 'DP008', 40.00, 'Pulsera con imagen de Jesús Cristo'), 
    ('Pulsera', 'DP009', 50.00, 'Pulsera de cuentas de piedra natural negra'), 
    ('Pulsera', 'DP010', 50.00, 'Pulsera de cuentas de piedra natural roja'), 
    ('Pulsera', 'DP011', 50.00, 'Pulsera con el Padre Nuestro'),
    ('Pulsera', 'DP012', 45.00, 'Pulsera reversible'),
    ('Pulsera', 'DP013', 28.00, 'Pulsera de hilo rojo con dije plata'),
    ('Pulsera', 'DP014', 38.00, 'Pulsera de hilo rojo con dije oro'),
    ('Pulsera', 'DP016', 50.00, 'Pulsera de xuping'),
    ('Pulsera', 'DP017', 50.00, 'Pulsera de xuping medalla milagrosa'),
    ('Pulsera', 'DP018', 60.00, 'Pulsera con billa de plata roja'),
    ('Pulsera', 'DP019', 60.00, 'Pulsera con billa de plata azul'),
    ('Pulsera', 'DP020', 45.00, 'Pulsera de piedra ojo de tigre'),
    ('Pulsera', 'DP021', 45.00, 'Pulsera de piedra volcanica'),
    ('Pulsera', 'DP022', 45.00, 'Pulsera de piedra howlita'),
    ('Pulsera', 'DP023', 45.00, 'Pulsera de jaspe madera'),
    ('Pulsera', 'DP024', 45.00, 'Pulsera de marfil'),
    ('Pulsera', 'DP025', 45.00, 'Pulsera de jaspe gris'),
    ('Pulsera', 'DP026', 45.00, 'Pulsera de piedra amazona'),
    ('Pulsera', 'DP027', 45.00, 'Pulsera de lapiz lazuli'),
    ('Pulsera', 'DP028', 45.00, 'Pulsera de piedra agata andina'),

    # Denarios
    ('Denario', 'TK001', 25.00, 'Denario Perla piña'), 
    ('Denario', 'TK002', 25.00, 'Denario para retrovisor de carro rojo'), 
    ('Denario', 'TK003', 25.00, 'Denario para retrovisor de carro azul'),
    ('Denario', 'TK004', 30.00, 'Denario de bolas de murano'),
    ('Denario', 'TK005', 22.00, 'Denario de bolas perladas de plástico'), 
    ('Denario', 'TK006', 15.00, 'Denario de bolas de madera'),
    ('Denario', 'TK007', 25.00, 'Denario de bolas de metal'),
    ('Denario', 'TK008', 15.70, 'Denario de Santa Clara'), 
    ('Denario', 'TK009', 16.50, 'Denario de San Pío de Pietrelcina'),
    ('Denario', 'TK010', 25.90, 'Denario de San Ignacio de Loyola')
]

# Datos fijos para Empresa, Courier, Comercial, Trabajador, Despacho y Producto
datos_fijos = {
    'empresas': [
        ('20546694969', 'San Benito-Articulos Religiosos', 'Jr. Francisco Javier Mariátegui 395', '986634385', 'Comercial'),
        ('23456789012', 'Proveedor 1', 'Calle Secundaria 456', '923456789', 'Comercial'), 
        ('34567890123', 'Proveedor 2', 'Calle Tercera 789', '934567890', 'Comercial'), 
        ('45678901234', 'Proveedor 3', 'Av. Cuarta 101', '945678901', 'Comercial'),
        ('56789012345', 'Proveedor 4', 'Av. Quinta 202', '956789012', 'Comercial'), 
        ('67890123456', 'Proveedor 5', 'Av. Sexta 303', '967890123', 'Comercial'), 
        ('89012345678', 'Dinsides', 'Av. Lima 505', '989012345', 'Courier'),
        ('90123456789', 'Olva', 'Av. Provincia 606', '990123456', 'Courier'),
        ('01234567890', 'Express', 'Av. Taxi 707', '991234567', 'Courier')
    ],
    'couriers': [
        ('89012345678',), ('90123456789',), ('01234567890',)
    ],
    'comerciales': [
        ('20546694969',), ('23456789012',), ('34567890123',),
        ('45678901234',), ('56789012345',), ('67890123456',)
    ],
    'personas_trabajadores': [
        ('30422817', 'Flavia Cuadros Teran', 21),
        ('29697994', 'Neymi Nadia Teran Delgado', 49),
        ('75573562', 'Cindy Lissel Teran Delgado', 41)
    ],
    'trabajadores': [
        ('30422817', 'flaviacuadros2001@gmail.com'),
        ('29697994', 'neyminadia76@gmail.com'),
        ('75573562', 'cindyteran@gmail.com')
    ],
    'despachos': [
        ('Av. Las Gaviotas 1805', '981008866'),
        ('Jr. Francisco Javier Mariátegui 395', '986634385')
    ]
}

# Generar datos generales
def generar_telefono():
    telefono = "9"
    for _ in range(8):
        telefono += str(random.randint(0, 9))
    return telefono

def generar_placa():
    letras = ''.join(random.choices(string.ascii_uppercase, k=3))
    numeros = ''.join(random.choices(string.digits, k=3))
    placa = f"{letras}-{numeros}"
    return placa

def generar_fecha():
    fecha_inicio = datetime(2019, 1, 1).date()
    fecha_fin = datetime(2023, 12, 31).date()
    diferencia = fecha_fin - fecha_inicio
    dias_totales = diferencia.days
    dias_aleatorios = random.randint(0, dias_totales)
    fecha_generada = fecha_inicio + timedelta(days=dias_aleatorios)
    return fecha_generada

def generar_fecha_hora_aleatoria():
    fecha_inicio = datetime(2019, 1, 1)
    fecha_actual = datetime.now()
    diferencia = fecha_actual - fecha_inicio
    segundos_totales = int(diferencia.total_seconds())
    segundos_aleatorios = random.randint(0, segundos_totales)
    fecha_hora_aleatoria = fecha_inicio + timedelta(seconds=segundos_aleatorios)
    return fecha_hora_aleatoria

def generar_direccion_random():
    direccion = fake.address()
    if len(direccion) > 200:
        direccion = direccion[:200]
    return direccion

# Para poblar tablas fijas
def insertar_datos_fijos():
    for empresa in datos_fijos['empresas']:
        cursor.execute("INSERT INTO Empresa (RUC, nombre, direccion, telefono, tipo) VALUES (%s, %s, %s, %s, %s)", empresa)
    for courier in datos_fijos['couriers']:
        cursor.execute("INSERT INTO Courier (Empresa_RUC) VALUES (%s)", courier)
    for comercial in datos_fijos['comerciales']:
        cursor.execute("INSERT INTO Comercial (Empresa_RUC) VALUES (%s)", comercial)
    for persona in datos_fijos['personas_trabajadores']:
        cursor.execute("INSERT INTO Persona (dni, nombre_completo, edad) VALUES (%s, %s, %s)", persona)
    for trabajador in datos_fijos['trabajadores']:
        cursor.execute("INSERT INTO Trabajador (Persona_DNI, correo) VALUES (%s, %s)", trabajador)
    for despacho in datos_fijos['despachos']:
        cursor.execute("INSERT INTO Despacho (direccion, nro_telefono) VALUES (%s, %s)", despacho)

def insert_productos_fijos():
    for producto in productos_fijos:
        cursor.execute("INSERT INTO Producto (modelo, codigo, precio, descripcion) VALUES (%s, %s, %s, %s)", producto)
    return productos_fijos

def generate_persona(n):
    personas = set()
    while len(personas) < n:
        dni = fake.unique.random_number(digits=8, fix_len=True)
        if dni not in personas:
            nombre_completo = fake.name()
            edad = fake.random_int(min=18, max=90)
            cursor.execute("INSERT INTO Persona (DNI, nombre_completo, edad) VALUES (%s, %s, %s)", (dni, nombre_completo, edad))
            personas.add(dni)
            print(f"Successfully inserted Persona with DNI {dni}")
    return list(personas)

def generate_cliente(n, personas_disponibles):
    clientes = set()
    while len(clientes) < n:
        dni = random.choice(personas_disponibles)
        if dni not in clientes:
            celular = generar_telefono()
            cursor.execute("INSERT INTO Cliente (Persona_DNI, celular) VALUES (%s, %s)", (dni, celular))
            clientes.add(dni)
            print(f"Successfully inserted Cliente with DNI {dni}")
    return list(clientes)

def generate_repartidor(n, personas_disponibles, empresas):
    repartidores = set()
    while len(repartidores) < n:
        dni = random.choice(personas_disponibles)
        if dni not in repartidores:
            calificacion = random.randint(1, 5)
            celular = generar_telefono()
            placa = generar_placa()
            courier_ruc = random.choice(empresas)
            cursor.execute("INSERT INTO Repartidor (Persona_DNI, calificacion, celular, placa_vehiculo, Courier_RUC) VALUES (%s, %s, %s, %s, %s)", (dni, calificacion, celular, placa, courier_ruc))
            repartidores.add(dni)
            print(f"Successfully inserted Repartidor with DNI {dni}")
    return list(repartidores)

def generate_orden_de_compra(n, empresas, despachos):
    ordenes = []
    for _ in range(n):
        codigo = fake.unique.random_number(digits=6, fix_len=True)
        empresa_ruc = random.choice(empresas)
        despacho_direccion = random.choice(despachos)
        fecha = generar_fecha()
        cursor.execute("INSERT INTO Orden_de_compra (codigo, Empresa_RUC, Despacho_direccion, fecha) VALUES (%s, %s, %s, %s)", (codigo, empresa_ruc, despacho_direccion, fecha))
        ordenes.append(codigo)
        print(f"Successfully inserted Orden de compra with codigo {codigo}")
    return ordenes

def generate_comprobante_de_pago(n):
    comprobantes = []
    for _ in range(n):
        codigo = fake.unique.random_number(digits=6, fix_len=True)
        cursor.execute("INSERT INTO Comprobante_de_pago (codigo) VALUES (%s)", (codigo,))
        comprobantes.append(codigo)
        print(f"Successfully inserted Comprobante de Pago with codigo {codigo}")
    return comprobantes

def generate_venta(n, repartidores, personas, comprobantes):
    ventas = []
    for _ in range(n):
        codigo = fake.unique.random_number(digits=6, fix_len=True)
        comprobante_codigo = random.choice(comprobantes)
        fecha = generar_fecha_hora_aleatoria()
        total = random.uniform(10, 100)
        costo_envio = random.uniform(1, 10)
        fecha_envio = generar_fecha_hora_aleatoria()
        estado = fake.random_element(elements=('Enviado', 'Entregado', 'Pendiente'))
        direccion_destino = generar_direccion_random()
        repartidor_dni = random.choice(repartidores)
        es_virtual = fake.boolean()
        persona_dni = random.choice(personas)
        cursor.execute("INSERT INTO Venta (codigo, Comprobante_de_pago_codigo, fecha, total, costo_envio, fecha_y_hora_envio, estado, direccion_destino, Repartidor_DNI, es_virtual, Persona_DNI) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (codigo, comprobante_codigo, fecha, total, costo_envio, fecha_envio, estado, direccion_destino, repartidor_dni, es_virtual, persona_dni))
        ventas.append((codigo, total))
        print(f"Successfully inserted Venta with codigo {codigo}")
    return ventas

def generate_abastecimiento(n, productos, ordenes):
    combinaciones_usadas = set()
    for _ in range(n):
        while True:
            orden_codigo = random.choice(ordenes)
            producto = random.choice(productos)
            if (orden_codigo, producto[0], producto[1]) not in combinaciones_usadas:
                combinaciones_usadas.add((orden_codigo, producto[0], producto[1]))
                break
        cantidad = random.randint(1, 100)
        cursor.execute("INSERT INTO Abastecimiento (Orden_de_compra_codigo, Producto_modelo, Producto_codigo, cantidad) VALUES (%s, %s, %s, %s)", (orden_codigo, producto[0], producto[1], cantidad))
        print(f"Successfully inserted Abastecimiento for Orden {orden_codigo} and Producto {producto[0]} - {producto[1]}")

def generate_stock(n, productos, despachos):
    for despacho in despachos:
        for producto in productos:
            cantidad = 10000000
            cursor.execute("INSERT INTO Stock (Producto_modelo, Producto_codigo, Despacho_direccion, cantidad) VALUES (%s, %s, %s, %s)", (producto[0], producto[1], despacho, cantidad))
            print(f"Successfully inserted Stock for Producto {producto[0]} - {producto[1]}")

def generate_item_vendido_bloques(n, productos, ventas, bloque=100000):
    combinaciones_usadas = set()
    total_registros = 0
    
    for _ in range(0, n, bloque):
        for _ in range(bloque):
            while True:
                producto = random.choice(productos)
                venta = random.choice(ventas)
                venta_codigo = venta[0]
                if (producto[0], producto[1], venta_codigo) not in combinaciones_usadas:
                    combinaciones_usadas.add((producto[0], producto[1], venta_codigo))
                    break
            venta_total = venta[1]
            cantidad = random.randint(1, 5)
            cursor.execute("SELECT cantidad FROM Stock WHERE Producto_modelo = %s AND Producto_codigo = %s LIMIT 1", (producto[0], producto[1]))
            stock = cursor.fetchone()
            if stock and stock[0] >= cantidad:
                subtotal = producto[2] * cantidad
                cursor.execute("INSERT INTO Item_vendido (Producto_modelo, Producto_codigo, Venta_codigo, cantidad, subtotal) VALUES (%s, %s, %s, %s, %s)", (producto[0], producto[1], venta_codigo, cantidad, subtotal))
                cursor.execute("UPDATE Venta SET total = total + %s WHERE codigo = %s", (subtotal, venta_codigo))
                print(f"Successfully inserted Item Vendido for Venta {venta_codigo} and Producto {producto[0]} - {producto[1]}")
                total_registros += 1
            else:
                print(f"Insufficient stock for Producto {producto[0]} - {producto[1]}")
        
        # Confirmar los cambios cada bloque
        conn.commit()
    
    return total_registros

def generate_pago(n, ventas, trabajadores):
    combinaciones_usadas = set()
    for _ in range(n):
        venta = random.choice(ventas)
        venta_codigo = venta[0]
        venta_total = venta[1]
        cursor.execute("SELECT SUM(monto) FROM Pago WHERE Venta_codigo = %s", (venta_codigo,))
        total_pagado = cursor.fetchone()[0] or 0
        monto_restante = venta_total - total_pagado
        if monto_restante <= 0:
            continue
        while True:
            metodo_pago = fake.random_element(elements=('Yape', 'Plin', 'Visa', 'MasterCard', 'Efectivo'))
            if (venta_codigo, metodo_pago) not in combinaciones_usadas:
                combinaciones_usadas.add((venta_codigo, metodo_pago))
                break
        monto = min(monto_restante, random.uniform(5, monto_restante))
        trabajador = random.choice(trabajadores)
        trabajador_dni = trabajador[0]  # Obtener el DNI del trabajador desde los datos fijos
        cursor.execute("INSERT INTO Pago (Venta_codigo, metodo_pago, Trabajador_DNI, monto) VALUES (%s, %s, %s, %s)", (venta_codigo, metodo_pago, trabajador_dni, monto))
        print(f"Successfully inserted Pago for Venta {venta_codigo}")

# Insertar datos fijos
insertar_datos_fijos()
productos = insert_productos_fijos()

#100K
# Generar y poblar tablas
personas = generate_persona(30000)          # Generar 300 registros para la tabla Persona
clientes = generate_cliente(20000, personas)           # Generar 200 registros para la tabla Cliente
repartidores = generate_repartidor(10000, [p for p in personas if p not in clientes], [e[0] for e in datos_fijos['empresas'] if e[4] == 'Courier']) # Generar 100 registros para la tabla Repartidor
ordenes = generate_orden_de_compra(10000, [e[0] for e in datos_fijos['empresas']], [d[0] for d in datos_fijos['despachos']]) # Generar 100 registros para la tabla Orden de compra
comprobantes = generate_comprobante_de_pago(10000)     # Generar 100 registros para la tabla Comprobante de pago
ventas = generate_venta(10000, repartidores, personas, comprobantes)  # Generar 100 registros para la tabla Venta
generate_stock(5000, productos, [d[0] for d in datos_fijos['despachos']])            # Generar stock inicial para productos en despachos
generate_abastecimiento(10000, productos, ordenes)    # Generar 100 registros para la tabla Abastecimiento
generate_item_vendido_bloques(10000, productos, ventas)       # Generar 100 registros para la tabla Item vendido
generate_pago(10000, ventas, datos_fijos['trabajadores'])            # Generar 100 registros para la tabla Pago

# Confirmar los cambios y cerrar la conexión
conn.commit()
cursor.close()
conn.close()


