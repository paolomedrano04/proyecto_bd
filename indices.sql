-- Índices para la primera consulta
CREATE INDEX idx_venta_fecha ON Venta USING btree(fecha);
CREATE INDEX idx_pago_trabajador_dni ON Pago USING btree(Trabajador_DNI);
CREATE INDEX idx_item_vendido_venta_codigo ON Item_vendido USING btree(Venta_codigo);

-- Índices para la segunda consulta
CREATE INDEX idx_producto_modelo_codigo ON Producto USING btree(modelo, codigo);
CREATE INDEX idx_item_vendido_producto_modelo_codigo ON Item_vendido USING btree(Producto_modelo, Producto_codigo);

-- Índices para la tercera consulta
CREATE INDEX idx_stock_producto_modelo_codigo ON Stock USING btree(Producto_modelo, Producto_codigo);
CREATE INDEX idx_stock_despacho_direccion ON Stock USING btree(Despacho_direccion);

-- Índices para la cuarta consulta
CREATE INDEX idx_venta_fecha ON Venta USING btree(fecha);
CREATE INDEX idx_pago_venta_codigo ON Pago USING btree(Venta_codigo);
CREATE INDEX idx_cliente_persona_dni ON Cliente USING btree(Persona_DNI);
