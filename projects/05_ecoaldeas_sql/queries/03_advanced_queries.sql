-- ============================================================================
-- ECOALDEAS CHILENAS — Queries avanzadas (nivel 3)
-- ============================================================================
-- Demuestra: window functions, CTEs múltiples, RANK, NTILE, percentiles,
-- self-joins, funciones analíticas
-- ============================================================================


-- Q1. Ranking de ecoaldeas por diversidad productiva (window functions)
WITH diversidad AS (
    SELECT
        e.ecovillage_id,
        e.name,
        e.region,
        COUNT(DISTINCT pr.product_type) AS tipos_distintos,
        SUM(pr.annual_value_clp) AS ingresos_totales
    FROM ecovillage e
    LEFT JOIN production pr ON pr.ecovillage_id = e.ecovillage_id
    GROUP BY e.ecovillage_id, e.name, e.region
)
SELECT
    name,
    region,
    tipos_distintos,
    ingresos_totales,
    RANK() OVER (ORDER BY tipos_distintos DESC, ingresos_totales DESC) AS rank_diversidad,
    RANK() OVER (ORDER BY ingresos_totales DESC) AS rank_ingresos,
    ROUND(100.0 * PERCENT_RANK() OVER (ORDER BY ingresos_totales), 1) AS percentil_ingresos
FROM diversidad
ORDER BY rank_diversidad;


-- Q2. Año pico de fundación de ecoaldeas y crecimiento acumulado
WITH fundaciones_anuales AS (
    SELECT
        founded_year,
        COUNT(*) AS nuevas_fundaciones
    FROM ecovillage
    GROUP BY founded_year
),
acumulado AS (
    SELECT
        founded_year,
        nuevas_fundaciones,
        SUM(nuevas_fundaciones) OVER (ORDER BY founded_year) AS total_acumulado
    FROM fundaciones_anuales
)
SELECT * FROM acumulado;


-- Q3. Productividad económica por hectárea (eficiencia territorial)
SELECT
    e.name AS ecoaldea,
    e.hectares,
    SUM(pr.annual_value_clp) AS ingresos_clp_anuales,
    ROUND((SUM(pr.annual_value_clp) / e.hectares)::numeric / 1000000, 2) AS millones_clp_por_hectarea,
    NTILE(3) OVER (ORDER BY (SUM(pr.annual_value_clp) / e.hectares)) AS tercil_productividad
FROM ecovillage e
JOIN production pr ON pr.ecovillage_id = e.ecovillage_id
GROUP BY e.ecovillage_id, e.name, e.hectares
ORDER BY millones_clp_por_hectarea DESC;


-- Q4. Análisis de retención: cuánto tiempo en promedio permanece un miembro
WITH antiguedad_miembros AS (
    SELECT
        e.name AS ecoaldea,
        m.code,
        m.join_year,
        EXTRACT(YEAR FROM CURRENT_DATE) - m.join_year AS anios_en_comunidad,
        ROW_NUMBER() OVER (PARTITION BY e.ecovillage_id ORDER BY m.join_year) AS orden_ingreso
    FROM member m
    JOIN ecovillage e ON e.ecovillage_id = m.ecovillage_id
    WHERE m.residency_type = 'permanente'
)
SELECT
    ecoaldea,
    COUNT(*) AS miembros_permanentes,
    ROUND(AVG(anios_en_comunidad)::numeric, 1) AS promedio_anios,
    MIN(anios_en_comunidad) AS minimo_anios,
    MAX(anios_en_comunidad) AS maximo_anios
FROM antiguedad_miembros
GROUP BY ecoaldea
ORDER BY promedio_anios DESC;


-- Q5. Análisis comparativo: actividades obligatorias vs opcionales por ecoaldea
WITH stats_actividades AS (
    SELECT
        e.name AS ecoaldea,
        SUM(CASE WHEN a.is_obligatory THEN 1 ELSE 0 END) AS obligatorias,
        SUM(CASE WHEN NOT a.is_obligatory THEN 1 ELSE 0 END) AS opcionales,
        COUNT(*) AS total
    FROM ecovillage e
    JOIN activity a ON a.ecovillage_id = e.ecovillage_id
    GROUP BY e.name
)
SELECT
    ecoaldea,
    obligatorias,
    opcionales,
    total,
    ROUND(100.0 * obligatorias / total, 1) AS pct_obligatorias,
    CASE
        WHEN obligatorias > opcionales THEN 'Estructurada'
        WHEN obligatorias = opcionales THEN 'Equilibrada'
        ELSE 'Flexible'
    END AS tipo_organizacion
FROM stats_actividades
ORDER BY pct_obligatorias DESC;
