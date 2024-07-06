
import psycopg2 

# Conectar a la base de datos
conn = psycopg2.connect(
    database="proyecto",
    user="postgres",
    password="ut3c1719",
    host="localhost",
    port="5432",
    options="-c search_path=bd1k"
)
cursor = conn.cursor()

conn.autocommit = True

# Comandos SQL para eliminar los datos de las tablas
truncate_commands = [
    "TRUNCATE TABLE Item_vendido CASCADE;",
    "TRUNCATE TABLE Pago CASCADE;",
    "TRUNCATE TABLE Venta CASCADE;",
    "TRUNCATE TABLE Abastecimiento CASCADE;",
    "TRUNCATE TABLE Stock CASCADE;",
    "TRUNCATE TABLE Comprobante_de_pago CASCADE;",
    "TRUNCATE TABLE Orden_de_compra CASCADE;",
    "TRUNCATE TABLE Repartidor CASCADE;",
    "TRUNCATE TABLE Cliente CASCADE;",
    "TRUNCATE TABLE Despacho CASCADE;",
    "TRUNCATE TABLE Producto CASCADE;",
    "TRUNCATE TABLE Empresa CASCADE;",
    "TRUNCATE TABLE Persona CASCADE;"
]

# Ejecutar los comandos
for command in truncate_commands:
    cursor.execute(command)
    print(f"Successfully executed: {command}")

# Confirmar los cambios y cerrar la conexión
conn.commit()
cursor.close()
conn.close()
