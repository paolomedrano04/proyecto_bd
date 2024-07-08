set search_path to bd1millon;
-- Consultas antiguas
-- Consulta 1
SELECT 
    t.Persona_DNI AS Trabajador,
    p.nombre_completo AS Nombre_Trabajador,
    (SELECT SUM(v.total)
     FROM Venta v
     WHERE v.codigo IN (SELECT pa.Venta_codigo
                        FROM Pago pa
                        WHERE pa.Trabajador_DNI = t.Persona_DNI)
       AND v.fecha BETWEEN '2024-01-01' AND '2024-12-31') AS Total_Ventas,
    (SELECT COUNT(iv.Producto_codigo)
     FROM Item_vendido iv
     WHERE iv.Venta_codigo IN (SELECT v.codigo
                               FROM Venta v
                               WHERE v.fecha BETWEEN '2024-01-01' AND '2024-12-31')
       AND iv.Venta_codigo IN (SELECT pa.Venta_codigo
                               FROM Pago pa
                               WHERE pa.Trabajador_DNI = t.Persona_DNI)) AS Cantidad_Productos_Vendidos
FROM 
    Trabajador t
INNER JOIN 
    Persona p ON t.Persona_DNI = p.DNI
ORDER BY 
    Total_Ventas DESC;

-- Consulta 2
SELECT 
    p.modelo AS Modelo_Producto,
    p.codigo AS Codigo_Producto,
    (SELECT SUM(iv.cantidad)
     FROM Item_vendido iv
     WHERE iv.Producto_modelo = p.modelo
       AND iv.Producto_codigo = p.codigo
       AND iv.Venta_codigo IN (SELECT v.codigo
                               FROM Venta v
                               WHERE v.fecha BETWEEN '2024-01-01' AND '2024-12-31')) AS Cantidad_Vendida
FROM 
    Producto p
WHERE 
    EXISTS (SELECT 1
            FROM Item_vendido iv
            WHERE iv.Producto_modelo = p.modelo
              AND iv.Producto_codigo = p.codigo
              AND iv.Venta_codigo IN (SELECT v.codigo
                                      FROM Venta v
                                      WHERE v.fecha BETWEEN '2024-01-01' AND '2024-12-31'))
GROUP BY 
    p.modelo, p.codigo
ORDER BY 
    Cantidad_Vendida DESC
LIMIT 5;

-- Consulta 3
SELECT 
    d.direccion AS Direccion_Despacho,
    p.modelo AS Modelo_Producto,
    p.codigo AS Codigo_Producto,
    (SELECT s.cantidad 
     FROM Stock s
     WHERE s.Producto_modelo = p.modelo
       AND s.Producto_codigo = p.codigo
       AND s.Despacho_direccion = d.direccion) AS Cantidad_En_Stock,
    ((SELECT s.cantidad 
      FROM Stock s
      WHERE s.Producto_modelo = p.modelo
        AND s.Producto_codigo = p.codigo
        AND s.Despacho_direccion = d.direccion) * p.precio) AS Valor_Total
FROM 
    Producto p
WHERE 
    EXISTS (SELECT 1
            FROM Stock s
            WHERE s.Producto_modelo = p.modelo
              AND s.Producto_codigo = p.codigo
              AND EXISTS (SELECT 1
                          FROM Despacho d
                          WHERE s.Despacho_direccion = d.direccion))
ORDER BY 
    Direccion_Despacho, Modelo_Producto, Codigo_Producto;

-- Índices para la Consulta 4
CREATE INDEX idx_cliente_persona_dni ON Cliente USING hash(Persona_DNI);
CREATE INDEX idx_persona_dni ON Persona USING hash(DNI);
CREATE INDEX idx_venta_persona_dni_fecha_codigo ON Venta USING btree(Persona_DNI, fecha, codigo);
CREATE INDEX idx_pago_venta_codigo_metodo_pago ON Pago USING hash(Venta_codigo, metodo_pago);

-- Consulta 4
SELECT 
    c.Persona_DNI AS Cliente,
    p.nombre_completo AS Nombre_Cliente,
    (SELECT COUNT(pa.metodo_pago)
     FROM Pago pa
     WHERE pa.Venta_codigo IN (SELECT v.codigo
                               FROM Venta v
                               WHERE v.Persona_DNI = c.Persona_DNI
                                 AND v.fecha BETWEEN '2024-01-01' AND '2024-12-31')
       AND pa.metodo_pago = outer_pa.metodo_pago) AS Numero_Pagos,
    outer_pa.metodo_pago AS Metodo_Pago,
    (SELECT SUM(pa.monto)
     FROM Pago pa
     WHERE pa.Venta_codigo IN (SELECT v.codigo
                               FROM Venta v
                               WHERE v.Persona_DNI = c.Persona_DNI
                                 AND v.fecha BETWEEN '2024-01-01' AND '2024-12-31')
       AND pa.metodo_pago = outer_pa.metodo_pago) AS Monto_Total
FROM 
    Cliente c
INNER JOIN 
    Persona p ON c.Persona_DNI = p.DNI
INNER JOIN 
    (SELECT DISTINCT metodo_pago
     FROM Pago pa
     WHERE pa.Venta_codigo IN (SELECT v.codigo
                               FROM Venta v
                               WHERE v.fecha BETWEEN '2024-01-01' AND '2024-12-31')) AS outer_pa
WHERE 
    EXISTS (SELECT 1
            FROM Venta v
            WHERE v.Persona_DNI = c.Persona_DNI
              AND v.fecha BETWEEN '2024-01-01' AND '2024-12-31')
GROUP BY 
    c.Persona_DNI, p.nombre_completo, outer_pa.metodo_pago
ORDER BY 
    Monto_Total DESC;




