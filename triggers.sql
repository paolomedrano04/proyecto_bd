set search_path to bd10k;
--------  Trigger para actualizar el stock cuando se realiza una venta
CREATE OR REPLACE FUNCTION actualizar_stock()
RETURNS TRIGGER AS $$
DECLARE
    stock_cantidad INT;
    despacho_direccion TEXT;
BEGIN
    SELECT cantidad, Despacho_direccion INTO stock_cantidad, despacho_direccion
    FROM Stock
    WHERE Producto_modelo = NEW.Producto_modelo 
      AND Producto_codigo = NEW.Producto_codigo 
    LIMIT 1;

    IF stock_cantidad < NEW.cantidad THEN
        RAISE EXCEPTION 'No hay suficiente stock para el producto % y código %', NEW.Producto_modelo, NEW.Producto_codigo;
    ELSE
        UPDATE Stock
        SET cantidad = cantidad - NEW.cantidad
        WHERE Producto_modelo = NEW.Producto_modelo 
          AND Producto_codigo = NEW.Producto_codigo 
          AND Despacho_direccion = despacho_direccion;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_actualizar_stock
AFTER INSERT ON Item_vendido
FOR EACH ROW
EXECUTE FUNCTION actualizar_stock();


----  Trigger para registrar la fecha y hora de inserción en la tabla Venta
CREATE OR REPLACE FUNCTION registrar_fecha_hora_venta()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha := NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_registrar_fecha_hora_venta
BEFORE INSERT ON Venta
FOR EACH ROW
EXECUTE FUNCTION registrar_fecha_hora_venta();

---- Trigger para validar que no se pueda insertar un Pago si el total de pagos excede el monto total de la Venta
CREATE OR REPLACE FUNCTION validar_monto_pago()
RETURNS TRIGGER AS $$
DECLARE
    total_pagos FLOAT;
BEGIN
    SELECT SUM(monto) INTO total_pagos FROM Pago WHERE Venta_codigo = NEW.Venta_codigo;
    IF (total_pagos + NEW.monto) > (SELECT total FROM Venta WHERE codigo = NEW.Venta_codigo) THEN
        RAISE EXCEPTION 'El total de pagos excede el monto total de la venta.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_validar_monto_pago
BEFORE INSERT ON Pago
FOR EACH ROW
EXECUTE FUNCTION validar_monto_pago();

---- Trigger para actualizar la calificación promedio de un Repartidor después de una nueva calificación
---- Trigger para actualizar la calificación promedio de un Repartidor después de una nueva venta
CREATE OR REPLACE FUNCTION actualizar_calificacion_repartidor()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Repartidor
    SET calificacion = (
        SELECT AVG(calificacion)
        FROM Repartidor
        WHERE Persona_DNI = NEW.Repartidor_DNI
    )
    WHERE Persona_DNI = NEW.Repartidor_DNI;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_actualizar_calificacion_repartidor
AFTER INSERT ON Venta
FOR EACH ROW
EXECUTE FUNCTION actualizar_calificacion_repartidor();


CREATE TRIGGER tr_actualizar_calificacion_repartidor
AFTER INSERT ON Venta
FOR EACH ROW
WHEN (NEW.calificacion IS NOT NULL)
EXECUTE FUNCTION actualizar_calificacion_repartidor();

