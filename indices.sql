-- Índices para la primera consulta
CREATE INDEX idx_venta_fecha_codigo ON Venta USING btree(fecha, codigo);
CREATE INDEX idx_pago_venta_codigo_trabajador_dni ON Pago USING btree(Venta_codigo, Trabajador_DNI);
CREATE INDEX idx_trabajador_persona_dni ON Trabajador USING btree(Persona_DNI);
CREATE INDEX idx_persona_dni ON Persona USING btree(DNI);
CREATE INDEX idx_item_vendido_venta_codigo ON Item_vendido USING btree(Venta_codigo);
CREATE INDEX idx_pago_trabajador_dni ON pago(Trabajador_DNI);
CREATE INDEX idx_venta_codigo ON venta(codigo);

-- Índices para la segunda consulta
CREATE INDEX idx_producto_modelo_codigo ON Producto USING btree(modelo, codigo);
CREATE INDEX idx_item_vendido_producto_modelo_codigo ON Item_vendido USING btree(Producto_modelo, Producto_codigo);
CREATE INDEX idx_venta_fecha ON Venta(fecha);

-- Índices para la tercera consulta
CREATE INDEX idx_stock_producto_modelo_codigo ON Stock USING btree(Producto_modelo, Producto_codigo);
CREATE INDEX idx_stock_despacho_direccion ON Stock USING btree(Despacho_direccion);
CREATE INDEX idx_despacho_direccion ON Despacho USING btree(direccion);
CREATE INDEX idx_stock_direccion_modelo_codigo ON Stock (Despacho_direccion, Producto_modelo, Producto_codigo);
CREATE INDEX idx_producto_modelo_codigo_precio ON Producto (modelo, codigo, precio);

-- Índices para la cuarta consulta
CREATE INDEX idx_pago_venta_codigo_metodo_pago ON Pago USING btree(Venta_codigo, metodo_pago);
CREATE INDEX idx_cliente_persona_dni ON Cliente USING btree(Persona_DNI);
