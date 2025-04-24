/* Insert data into tables */

/* ORGANISMOS SECTORIALES */

INSERT INTO reportes_sma.reportes_organismosectorial (nombre, contacto, telefono) VALUES
('SEA',   'Servicio de Evaluación Ambiental',                         '+56911111111'),
('SEC',   'Superintendencia de Electricidad y Combustible',          '+56922222222'),
('IRV',   'Intendencia Regional de Valparaíso',                      '+56933333333'),
('DGTM',  'Dirección Gral. Territorio Marítimo y Marina Mercante',   '+56944444444'),
('CONAF', 'Corporación Nacional Forestal',                           '+56955555555'),
('SAG',   'Servicio Agrícola y Ganadero',                            '+56966666666'),
('SMA',   'Superintendencia del Medio Ambiente',                     '+56977777777');


/* MEDIDAS PDA */
INSERT INTO reportes_sma.reportes_medida (nombre, tipo, descripcion, fecha_inicio, fecha_termino, prioridad, organismo_responsable_id) VALUES
('Reemplazo de calefactores a leña en zonas críticas', 'Residencial', 'Recambio masivo de calefactores a leña por sistemas más eficientes y menos contaminantes en las comunas de la Región de Valparaíso.', '2025-05-01', '2027-12-31', 'Alta', 1),
('Restricción vehicular para vehículos antiguos', 'Transporte', 'Implementación de restricciones vehiculares para vehículos con más de 10 años de antigüedad en días con mala calidad del aire en la Región de Valparaíso.', '2025-04-15', '2030-12-31', 'Alta', 2),
('Monitoreo continuo de emisiones industriales', 'Industria', 'Instalación de sistemas de monitoreo continuo de emisiones para fuentes industriales en áreas urbanas de la Región de Valparaíso.', '2025-06-01', '2027-12-31', 'Alta', 3),
('Promoción del transporte público eléctrico', 'Transporte', 'Fomento de la electrificación del transporte público en las principales ciudades de la Región de Valparaíso, con buses eléctricos y estaciones de carga.', '2025-07-01', '2028-12-31', 'Media', 4),
('Campañas educativas sobre uso responsable de la leña', 'Gestión', 'Campañas de sensibilización sobre los riesgos del uso ineficiente de la leña y promoción de alternativas de calefacción más limpias en la región.', '2025-03-01', '2026-12-31', 'Baja', 5),
('Reforestación y arborización urbana', 'Gestión', 'Implementación de proyectos de reforestación y arborización en áreas urbanas de la región para mejorar la calidad del aire y reducir el polvo atmosférico.', '2025-08-01', '2027-12-31', 'Media', 6),
('Fiscalización de emisiones vehiculares', 'Transporte', 'Fortalecimiento de la fiscalización de emisiones vehiculares, especialmente en vehículos diésel, en la Región de Valparaíso.', '2025-05-01', '2027-12-31', 'Alta', 7),
('Rehabilitación de fuentes hídricas contaminadas', 'Gestión', 'Recuperación de cuerpos de agua contaminados por metales pesados en la Región de Valparaíso, mediante técnicas de biorremediación.', '2025-06-01', '2028-12-31', 'Media', 8),
('Normativa para la reducción de emisiones en la minería', 'Industria', 'Implementación de medidas estrictas para reducir las emisiones de partículas y gases contaminantes provenientes de las actividades mineras.', '2025-07-01', '2027-12-31', 'Alta', 9),
('Creación de zonas verdes en áreas urbanas', 'Gestión', 'Desarrollo de nuevas zonas verdes y parques urbanos en la Región de Valparaíso para mejorar la calidad del aire y la salud pública.', '2025-09-01', '2028-09-01', 'Media', 10);


/* PLANES DE DESCONTAMINACIÓN AMBIENTAL */

INSERT INTO reportes_sma.reportes_ppda (nombre, descripcion, fecha_inicio, fecha_termino, organismo_id) VALUES
('Plan de Recambio de Calefactores', 'Implementación de un plan de recambio de calefactores a leña en las comunas más afectadas por la contaminación en la Región de Valparaíso. El objetivo es reducir las emisiones de material particulado proveniente de fuentes residenciales.', '2025-05-01', '2027-12-31', 1),
('Plan de Monitoreo de Calidad del Aire', 'Desarrollo de un sistema de monitoreo continuo y en tiempo real de la calidad del aire en diferentes comunas de la Región de Valparaíso, con especial énfasis en zonas industriales y urbanas.', '2025-04-01', '2027-12-31', 2),
('Plan de Restricción Vehicular en Zonas Críticas', 'Implementación de restricciones vehiculares para vehículos con más de 10 años de antigüedad durante días de alta contaminación en las zonas más críticas de la Región de Valparaíso.', '2025-06-01', '2030-12-31', 3),
('Plan de Arborización y Reforestación Urbana', 'Lanzamiento de un plan de reforestación y arborización en las áreas urbanas de la Región de Valparaíso, para aumentar la captación de CO2 y mejorar la calidad del aire en zonas con alta densidad poblacional.', '2025-07-01', '2027-12-31', 4),
('Plan de Promoción de Energías Renovables', 'Fomento del uso de energías renovables en hogares e industrias de la Región de Valparaíso mediante incentivos y subsidios para la instalación de sistemas fotovoltaicos y solares térmicos, con el fin de reducir la dependencia de fuentes contaminantes.', '2025-08-01', '2028-12-31', 5);


/* ROLES */

INSERT INTO reportes_sma.reportes_perfilusuario (rol, user_id) VALUES
('Administrador', 1),
('Supervisor', 2),
('Operador', 3),
('Analista', 4),
('Auditor', 5);


INSERT INTO reportes_sma.reportes_indicador; (nombre, descripcion, valor, unidad, fecha_registro, medio_verificacion, organismo_sectorial_id, ppda_id) VALUES 
('Reducción de emisiones por calefactores', 'Porcentaje de reducción de emisiones de material particulado gracias al recambio de calefactores a leña en la Región de Valparaíso.', 25.5, 'Porcentaje', '2025-05-01', 'Informe de emisiones anuales', 1, 1),
('Número de vehículos restringidos', 'Cantidad de vehículos con más de 10 años de antigüedad restringidos durante días con alta contaminación en la Región de Valparaíso.', 1500, 'Vehículos', '2025-06-01', 'Reporte de control vehicular', 2, 2),
('Niveles de contaminación monitoreados', 'Promedio de niveles de contaminación monitoreados en diferentes estaciones en la Región de Valparaíso durante el año.', 120, 'µg/m³', '2025-04-01', 'Informe de monitoreo ambiental', 3, 3),
('Área de reforestación urbana', 'Cantidad de área urbana reforestada para mejorar la calidad del aire y captación de CO2 en la Región de Valparaíso.', 50.0, 'Hectáreas', '2025-07-01', 'Informe de progreso del proyecto', 4, 4),
('Instalación de paneles solares', 'Número de instalaciones de paneles solares realizadas en hogares e industrias en la Región de Valparaíso como parte del fomento de energías renovables.', 300, 'Instalaciones', '2025-08-01', 'Informe de instalaciones', 5, 5);

