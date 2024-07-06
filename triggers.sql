set search_path to bd1k;
--------  Trigger para actualizar el stock cuando se realiza una venta
CREATE OR REPLACE FUNCTION actualizar_stock()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT cantidad FROM Stock 
        WHERE Producto_modelo = NEW.Producto_modelo 
        AND Producto_codigo = NEW.Producto_codigo 
        AND Despacho_direccion = (SELECT Despacho_direccion 
                                  FROM Stock 
                                  WHERE Producto_modelo = NEW.Producto_modelo 
                                  AND Producto_codigo = NEW.Producto_codigo LIMIT 1)
       ) < NEW.cantidad THEN
        RAISE EXCEPTION 'No hay suficiente stock para el producto % y código %', NEW.Producto_modelo, NEW.Producto_codigo;
    ELSE
        UPDATE Stock
        SET cantidad = cantidad - NEW.cantidad
        WHERE Producto_modelo = NEW.Producto_modelo 
        AND Producto_codigo = NEW.Producto_codigo 
        AND Despacho_direccion = (SELECT Despacho_direccion 
                                  FROM Stock 
                                  WHERE Producto_modelo = NEW.Producto_modelo 
                                  AND Producto_codigo = NEW.Producto_codigo LIMIT 1);
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

