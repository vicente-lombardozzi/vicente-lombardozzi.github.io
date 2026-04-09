-- ============================================================================
-- ECOALDEAS CHILENAS — Datos de ejemplo (anonimizados)
-- ============================================================================
--
-- Datos sintéticos basados en investigación real del autor sobre ecoaldeas
-- chilenas, con nombres reales modificados para proteger la privacidad.
--
-- ============================================================================

-- Roles
INSERT INTO role (name, description) VALUES
    ('coordinador_general', 'Coordinador general de la asamblea o consejo'),
    ('tesorero', 'Encargado de la gestión económica de la comunidad'),
    ('huerta', 'Responsable de los espacios productivos agrícolas'),
    ('educacion', 'Coordinador de actividades educativas internas y externas'),
    ('mantencion', 'Responsable de mantención de infraestructura'),
    ('hospedaje', 'Coordinador de visitas y voluntarios'),
    ('miembro_general', 'Miembro sin rol específico de coordinación');

-- Categorías de actividades
INSERT INTO activity_category (name, description) VALUES
    ('produccion_agricola', 'Huertas, invernaderos, cuidado de animales'),
    ('construccion', 'Bioconstrucción, mantención, infraestructura'),
    ('educacion', 'Talleres, cursos, formación interna y externa'),
    ('asambleas', 'Reuniones de toma de decisiones colectivas'),
    ('cuidados', 'Cocina común, cuidado de niños, salud comunitaria'),
    ('espiritualidad', 'Prácticas espirituales, meditación, ceremonias'),
    ('turismo_pedagogico', 'Recepción de visitas educativas y voluntarios');

-- Ecoaldeas (5 casos chilenos representativos, datos anonimizados)
INSERT INTO ecovillage (name, region, province, commune, founded_year, hectares, legal_status, governance_model, description) VALUES
    ('Comunidad Crisálida', 'Valparaíso', 'Marga Marga', 'Olmué', 1995, 12.5, 'fundación', 'consenso', 'Una de las ecoaldeas pioneras de Chile, fundada en los años 90'),
    ('Aldea El Manzano', 'Biobío', 'Concepción', 'Cabrero', 2000, 25.0, 'cooperativa', 'sociocracia', 'Comunidad rural enfocada en bioconstrucción y permacultura'),
    ('Comunidad Pewkayal', 'Los Ríos', 'Valdivia', 'Panguipulli', 2003, 40.0, 'fundación', 'asamblea horizontal', 'Ecoaldea ubicada en la selva valdiviana, fuerte componente indigenista'),
    ('Bosque Nativo', 'La Araucanía', 'Cautín', 'Pucón', 2007, 18.0, 'sin formalización', 'consenso', 'Comunidad joven enfocada en regeneración de bosque nativo'),
    ('Tierra Viva', 'Maule', 'Talca', 'San Clemente', 2012, 8.0, 'cooperativa', 'sociocracia', 'Ecoaldea pequeña con fuerte orientación productiva agroecológica');

-- Miembros (datos sintéticos)
INSERT INTO member (ecovillage_id, code, join_year, residency_type, age_group, role_id, is_founder) VALUES
    (1, 'CRI-001', 1995, 'permanente', '45-64', 1, TRUE),
    (1, 'CRI-002', 1995, 'permanente', '45-64', 2, TRUE),
    (1, 'CRI-003', 1998, 'permanente', '30-44', 3, FALSE),
    (1, 'CRI-004', 2005, 'permanente', '30-44', 4, FALSE),
    (1, 'CRI-005', 2010, 'permanente', '18-29', 7, FALSE),
    (1, 'CRI-006', 2015, 'temporal', '18-29', 7, FALSE),
    (2, 'MAN-001', 2000, 'permanente', '45-64', 1, TRUE),
    (2, 'MAN-002', 2000, 'permanente', '30-44', 5, TRUE),
    (2, 'MAN-003', 2002, 'permanente', '30-44', 3, FALSE),
    (2, 'MAN-004', 2008, 'permanente', '30-44', 4, FALSE),
    (2, 'MAN-005', 2012, 'permanente', '18-29', 7, FALSE),
    (3, 'PEW-001', 2003, 'permanente', '45-64', 1, TRUE),
    (3, 'PEW-002', 2003, 'permanente', '45-64', 2, TRUE),
    (3, 'PEW-003', 2005, 'permanente', '30-44', 6, FALSE),
    (3, 'PEW-004', 2009, 'permanente', '30-44', 3, FALSE),
    (3, 'PEW-005', 2013, 'permanente', '18-29', 7, FALSE),
    (3, 'PEW-006', 2017, 'temporal', '18-29', 7, FALSE),
    (3, 'PEW-007', 2018, 'temporal', '18-29', 7, FALSE),
    (4, 'BOS-001', 2007, 'permanente', '30-44', 1, TRUE),
    (4, 'BOS-002', 2007, 'permanente', '30-44', 3, TRUE),
    (4, 'BOS-003', 2011, 'permanente', '18-29', 7, FALSE),
    (5, 'TIE-001', 2012, 'permanente', '30-44', 1, TRUE),
    (5, 'TIE-002', 2012, 'permanente', '30-44', 3, TRUE),
    (5, 'TIE-003', 2014, 'permanente', '30-44', 5, FALSE),
    (5, 'TIE-004', 2018, 'permanente', '18-29', 7, FALSE);

-- Actividades
INSERT INTO activity (ecovillage_id, category_id, name, frequency, is_obligatory) VALUES
    (1, 1, 'Huerta orgánica', 'diaria', TRUE),
    (1, 4, 'Asamblea semanal', 'semanal', TRUE),
    (1, 7, 'Recepción de visitantes', 'semanal', FALSE),
    (1, 5, 'Cocina común', 'diaria', TRUE),
    (1, 3, 'Talleres educativos abiertos', 'mensual', FALSE),
    (2, 1, 'Permacultura', 'diaria', TRUE),
    (2, 2, 'Bioconstrucción', 'semanal', FALSE),
    (2, 4, 'Asamblea quincenal', 'semanal', TRUE),
    (2, 5, 'Cocina comunitaria', 'diaria', TRUE),
    (3, 1, 'Cuidado del bosque', 'diaria', TRUE),
    (3, 6, 'Ceremonias estacionales', 'estacional', FALSE),
    (3, 4, 'Asamblea mensual', 'mensual', TRUE),
    (3, 7, 'Programa de voluntariado', 'semanal', FALSE),
    (4, 1, 'Reforestación nativa', 'semanal', TRUE),
    (4, 4, 'Asamblea semanal', 'semanal', TRUE),
    (5, 1, 'Producción agroecológica', 'diaria', TRUE),
    (5, 4, 'Asamblea semanal', 'semanal', TRUE);

-- Participación (horas semanales por miembro/actividad)
INSERT INTO participation (member_id, activity_id, hours_per_week) VALUES
    (1, 1, 15), (1, 2, 4), (1, 4, 8),
    (2, 2, 4), (2, 4, 12),
    (3, 1, 30), (3, 2, 4),
    (4, 5, 10), (4, 4, 4), (4, 2, 4),
    (5, 1, 12), (5, 3, 6), (5, 4, 4),
    (6, 3, 20), (6, 1, 8),
    (7, 6, 20), (7, 8, 6),
    (8, 7, 25), (8, 8, 6),
    (9, 6, 25), (9, 9, 10),
    (10, 8, 8), (10, 6, 10),
    (11, 6, 15), (11, 9, 10),
    (12, 12, 8), (12, 11, 4),
    (13, 11, 12), (13, 12, 4),
    (14, 11, 10),
    (15, 10, 25), (15, 12, 4),
    (16, 13, 30), (16, 10, 8),
    (17, 13, 25), (17, 10, 12),
    (18, 13, 30), (18, 10, 8),
    (19, 14, 25), (19, 15, 6),
    (20, 14, 28), (20, 15, 6),
    (21, 14, 30),
    (22, 16, 25), (22, 17, 6),
    (23, 16, 28), (23, 17, 6),
    (24, 17, 8), (24, 16, 12),
    (25, 16, 30);

-- Recursos
INSERT INTO resource (ecovillage_id, type, quantity, unit, is_self_produced, measured_year) VALUES
    (1, 'agua_potable', 18000, 'L/dia', TRUE, 2023),
    (1, 'energia_solar', 8500, 'kWh/anio', TRUE, 2023),
    (1, 'biomasa_lena', 2500, 'kg/anio', TRUE, 2023),
    (2, 'agua_potable', 25000, 'L/dia', TRUE, 2023),
    (2, 'energia_solar', 12000, 'kWh/anio', TRUE, 2023),
    (2, 'energia_eolica', 4500, 'kWh/anio', TRUE, 2023),
    (3, 'agua_potable', 30000, 'L/dia', TRUE, 2023),
    (3, 'energia_hidroelectrica', 15000, 'kWh/anio', TRUE, 2023),
    (4, 'agua_potable', 12000, 'L/dia', TRUE, 2023),
    (4, 'energia_solar', 6000, 'kWh/anio', TRUE, 2023),
    (5, 'agua_potable', 8000, 'L/dia', TRUE, 2023),
    (5, 'energia_solar', 4500, 'kWh/anio', TRUE, 2023);

-- Producción
INSERT INTO production (ecovillage_id, product_name, product_type, annual_value_clp, is_for_sale, is_for_self_consumption) VALUES
    (1, 'Verduras organicas', 'alimento', 6500000, TRUE, TRUE),
    (1, 'Talleres de permacultura', 'educacion', 4200000, TRUE, FALSE),
    (1, 'Hospedaje', 'turismo', 3800000, TRUE, FALSE),
    (2, 'Frutas y verduras', 'alimento', 8200000, TRUE, TRUE),
    (2, 'Cursos de bioconstruccion', 'educacion', 6800000, TRUE, FALSE),
    (2, 'Mermeladas y conservas', 'alimento', 2400000, TRUE, TRUE),
    (3, 'Hierbas medicinales', 'alimento', 3200000, TRUE, TRUE),
    (3, 'Artesania mapuche', 'artesania', 2800000, TRUE, FALSE),
    (3, 'Turismo etnico', 'turismo', 7500000, TRUE, FALSE),
    (3, 'Voluntariado pago', 'turismo', 4200000, TRUE, FALSE),
    (4, 'Plantas nativas', 'alimento', 1800000, TRUE, FALSE),
    (4, 'Consultoria reforestacion', 'consultoria', 3500000, TRUE, FALSE),
    (5, 'Verduras certificadas', 'alimento', 5200000, TRUE, FALSE),
    (5, 'Mermeladas artesanales', 'alimento', 1800000, TRUE, TRUE);
