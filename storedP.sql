-- Crear procedimientos almacenados necesarios
CREATE OR REPLACE FUNCTION registrar_venta(
    p_codigo INT,
    p_fecha TIMESTAMP,
    p_total FLOAT,
    p_costo_envio FLOAT,
    p_fecha_y_hora_envio TIMESTAMP,
    p_estado VARCHAR(10),
    p_direccion_destino VARCHAR(100),
    p_repartidor_dni VARCHAR(8),
    p_es_virtual BOOLEAN,
    p_persona_dni VARCHAR(8),
    p_items JSON
)
RETURNS VOID AS $$
DECLARE
    item JSON;
    prod_modelo VARCHAR(10);
    prod_codigo VARCHAR(4);
    cantidad INT;
    subtotal FLOAT;
BEGIN
    -- Insertar en la tabla Venta
    INSERT INTO Venta (codigo, fecha, total, costo_envio, fecha_y_hora_envio, estado, direccion_destino, Repartidor_DNI, es_virtual, Persona_DNI)
    VALUES (p_codigo, p_fecha, p_total, p_costo_envio, p_fecha_y_hora_envio, p_estado, p_direccion_destino, p_repartidor_dni, p_es_virtual, p_persona_dni);
    
    -- Insertar en la tabla Item_vendido y actualizar el stock
    FOR item IN SELECT * FROM json_array_elements(p_items) LOOP
        prod_modelo := item->>'Producto_modelo';
        prod_codigo := item->>'Producto_codigo';
        cantidad := (item->>'cantidad')::INT;
        subtotal := (item->>'subtotal')::FLOAT;
        
        INSERT INTO Item_vendido (Producto_modelo, Producto_codigo, Venta_codigo, cantidad, subtotal)
        VALUES (prod_modelo, prod_codigo, p_codigo, cantidad, subtotal);
        
        UPDATE Stock
        SET cantidad = cantidad - cantidad
        WHERE Producto_modelo = prod_modelo AND Producto_codigo = prod_codigo AND Despacho_direccion = (SELECT direccion FROM Despacho LIMIT 1);
    END LOOP;
    
END;
$$ LANGUAGE plpgsql;
