-- ============================================================================
-- ECOALDEAS CHILENAS — Base de datos relacional
-- ============================================================================
--
-- Diseño y modelado de una base de datos relacional para gestionar información
-- sobre comunidades ecológicas (ecoaldeas) en Chile, basado en investigación
-- académica del autor sobre el tema (MSc University of Leeds 2019 + libro
-- publicado en Editorial Académica Española 2017).
--
-- Compatible con PostgreSQL 14+ y SQLite 3.35+
--
-- Autor: Vicente Lombardozzi
-- Fecha: 2026
-- ============================================================================

-- Limpiar tablas existentes (orden inverso a las dependencias)
DROP TABLE IF EXISTS production CASCADE;
DROP TABLE IF EXISTS participation CASCADE;
DROP TABLE IF EXISTS resource CASCADE;
DROP TABLE IF EXISTS member CASCADE;
DROP TABLE IF EXISTS activity CASCADE;
DROP TABLE IF EXISTS activity_category CASCADE;
DROP TABLE IF EXISTS role CASCADE;
DROP TABLE IF EXISTS ecovillage CASCADE;

-- ============================================================================
-- 1. Ecoaldeas (entidad principal)
-- ============================================================================
CREATE TABLE ecovillage (
    ecovillage_id     SERIAL PRIMARY KEY,
    name              VARCHAR(120) NOT NULL UNIQUE,
    region            VARCHAR(80) NOT NULL,
    province          VARCHAR(80),
    commune           VARCHAR(80),
    founded_year      INTEGER NOT NULL CHECK (founded_year BETWEEN 1900 AND 2100),
    hectares          NUMERIC(10, 2) CHECK (hectares > 0),
    legal_status      VARCHAR(40),  -- e.g., 'fundación', 'cooperativa', 'sin formalización'
    governance_model  VARCHAR(60),  -- e.g., 'sociocracia', 'consenso', 'asamblea horizontal'
    website           VARCHAR(200),
    description       TEXT,
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ecovillage_region ON ecovillage(region);
CREATE INDEX idx_ecovillage_year ON ecovillage(founded_year);

-- ============================================================================
-- 2. Roles que pueden cumplir los miembros
-- ============================================================================
CREATE TABLE role (
    role_id      SERIAL PRIMARY KEY,
    name         VARCHAR(60) NOT NULL UNIQUE,
    description  TEXT
);

-- ============================================================================
-- 3. Miembros de las ecoaldeas
-- ============================================================================
CREATE TABLE member (
    member_id          SERIAL PRIMARY KEY,
    ecovillage_id      INTEGER NOT NULL REFERENCES ecovillage(ecovillage_id) ON DELETE CASCADE,
    code               VARCHAR(20) NOT NULL,  -- pseudonimizado para privacidad
    join_year          INTEGER NOT NULL,
    residency_type     VARCHAR(40),  -- 'permanente', 'temporal', 'visitante regular'
    age_group          VARCHAR(20),  -- '18-29', '30-44', '45-64', '65+'
    role_id            INTEGER REFERENCES role(role_id),
    is_founder         BOOLEAN DEFAULT FALSE,
    UNIQUE (ecovillage_id, code)
);

CREATE INDEX idx_member_ecovillage ON member(ecovillage_id);
CREATE INDEX idx_member_role ON member(role_id);

-- ============================================================================
-- 4. Categorías de actividades
-- ============================================================================
CREATE TABLE activity_category (
    category_id   SERIAL PRIMARY KEY,
    name          VARCHAR(60) NOT NULL UNIQUE,
    description   TEXT
);

-- ============================================================================
-- 5. Actividades que se realizan en las ecoaldeas
-- ============================================================================
CREATE TABLE activity (
    activity_id     SERIAL PRIMARY KEY,
    ecovillage_id   INTEGER NOT NULL REFERENCES ecovillage(ecovillage_id) ON DELETE CASCADE,
    category_id     INTEGER NOT NULL REFERENCES activity_category(category_id),
    name            VARCHAR(120) NOT NULL,
    description     TEXT,
    frequency       VARCHAR(40),  -- 'diaria', 'semanal', 'mensual', 'estacional'
    is_obligatory   BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_activity_ecovillage ON activity(ecovillage_id);
CREATE INDEX idx_activity_category ON activity(category_id);

-- ============================================================================
-- 6. Participación: tabla puente entre miembros y actividades
-- ============================================================================
CREATE TABLE participation (
    participation_id  SERIAL PRIMARY KEY,
    member_id         INTEGER NOT NULL REFERENCES member(member_id) ON DELETE CASCADE,
    activity_id       INTEGER NOT NULL REFERENCES activity(activity_id) ON DELETE CASCADE,
    hours_per_week    NUMERIC(5, 2) CHECK (hours_per_week >= 0),
    start_date        DATE,
    end_date          DATE,
    UNIQUE (member_id, activity_id)
);

CREATE INDEX idx_participation_member ON participation(member_id);
CREATE INDEX idx_participation_activity ON participation(activity_id);

-- ============================================================================
-- 7. Recursos materiales y energéticos de cada ecoaldea
-- ============================================================================
CREATE TABLE resource (
    resource_id     SERIAL PRIMARY KEY,
    ecovillage_id   INTEGER NOT NULL REFERENCES ecovillage(ecovillage_id) ON DELETE CASCADE,
    type            VARCHAR(60) NOT NULL,  -- 'agua', 'energía solar', 'biomasa', etc.
    quantity        NUMERIC(12, 3),
    unit            VARCHAR(20),  -- 'L', 'kWh', 'kg', 'm³'
    is_self_produced BOOLEAN DEFAULT FALSE,
    measured_year   INTEGER
);

CREATE INDEX idx_resource_ecovillage ON resource(ecovillage_id);
CREATE INDEX idx_resource_type ON resource(type);

-- ============================================================================
-- 8. Producción económica de las ecoaldeas
-- ============================================================================
CREATE TABLE production (
    production_id    SERIAL PRIMARY KEY,
    ecovillage_id    INTEGER NOT NULL REFERENCES ecovillage(ecovillage_id) ON DELETE CASCADE,
    product_name     VARCHAR(120) NOT NULL,
    product_type     VARCHAR(60),  -- 'alimento', 'artesanía', 'turismo', 'educación', 'consultoría'
    annual_value_clp BIGINT,
    is_for_sale      BOOLEAN DEFAULT TRUE,
    is_for_self_consumption BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_production_ecovillage ON production(ecovillage_id);
CREATE INDEX idx_production_type ON production(product_type);

-- ============================================================================
-- COMENTARIOS DE DISEÑO
-- ============================================================================
--
-- 1. Pseudonimización: los miembros se identifican por código interno, no por
--    nombre real, para proteger la privacidad de los participantes (consistente
--    con los principios éticos de la investigación social aplicada).
--
-- 2. SERIAL como PK: usamos auto-incremento porque facilita inserts y joins,
--    aunque para producción real se podría considerar UUIDs.
--
-- 3. CASCADE en relaciones: si se elimina una ecoaldea, se eliminan sus
--    miembros, actividades, etc. Reflejá la dependencia ontológica.
--
-- 4. Índices: agregados en columnas usadas frecuentemente en JOINs y WHEREs
--    para análisis exploratorio.
--
-- 5. CHECK constraints: validación a nivel de base de datos para garantizar
--    integridad de los datos numéricos.
