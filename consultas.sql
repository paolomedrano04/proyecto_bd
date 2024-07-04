-- Consulta 1
SELECT 
    t.Persona_DNI AS Trabajador,
    p.nombre_completo AS Nombre_Trabajador,
    SUM(v.total) AS Total_Ventas,
    COUNT(iv.Producto_codigo) AS Cantidad_Productos_Vendidos
FROM 
    Venta v
JOIN 
    Pago pa ON v.codigo = pa.Venta_codigo
JOIN 
    Trabajador t ON pa.Trabajador_DNI = t.Persona_DNI
JOIN 
    Persona p ON t.Persona_DNI = p.DNI
JOIN 
    Item_vendido iv ON v.codigo = iv.Venta_codigo
WHERE 
    v.fecha BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY 
    t.Persona_DNI, p.nombre_completo
ORDER BY 
    Total_Ventas DESC;

-- Consulta 2
-- Productos más vendidos
SELECT 
    p.modelo AS Modelo_Producto,
    p.codigo AS Codigo_Producto,
    SUM(iv.cantidad) AS Cantidad_Vendida
FROM 
    Producto p
JOIN 
    Item_vendido iv ON p.modelo = iv.Producto_modelo AND p.codigo = iv.Producto_codigo
JOIN 
    Venta v ON iv.Venta_codigo = v.codigo
WHERE 
    v.fecha BETWEEN '2024-01-01' AND '2024-12-31'
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
    s.cantidad AS Cantidad_En_Stock,
    (s.cantidad * p.precio) AS Valor_Total
FROM 
    Stock s
JOIN 
    Producto p ON s.Producto_modelo = p.modelo AND s.Producto_codigo = p.codigo
JOIN 
    Despacho d ON s.Despacho_direccion = d.direccion
ORDER BY 
    d.direccion, p.modelo, p.codigo;

-- Consulta 4
SELECT 
    c.Persona_DNI AS Cliente,
    p.nombre_completo AS Nombre_Cliente,
    COUNT(pa.metodo_pago) AS Numero_Pagos,
    pa.metodo_pago AS Metodo_Pago,
    SUM(pa.monto) AS Monto_Total
FROM 
    Venta v
JOIN 
    Pago pa ON v.codigo = pa.Venta_codigo
JOIN 
    Cliente c ON v.Persona_DNI = c.Persona_DNI
JOIN 
    Persona p ON c.Persona_DNI = p.DNI
WHERE 
    v.fecha BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY 
    c.Persona_DNI, p.nombre_completo, pa.metodo_pago
ORDER BY 
    Monto_Total DESC;

