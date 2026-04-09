-- ============================================================================
-- ECOALDEAS CHILENAS — Queries intermedias (nivel 2)
-- ============================================================================
-- Demuestra: JOINs múltiples, GROUP BY con HAVING, subconsultas, CTEs simples
-- ============================================================================


-- Q1. Promedio de horas semanales dedicadas por categoría de actividad y región
SELECT
    e.region,
    ac.name AS categoria_actividad,
    ROUND(AVG(p.hours_per_week)::numeric, 2) AS promedio_horas_semanales,
    COUNT(p.participation_id) AS num_participaciones
FROM participation p
JOIN member m ON m.member_id = p.member_id
JOIN ecovillage e ON e.ecovillage_id = m.ecovillage_id
JOIN activity a ON a.activity_id = p.activity_id
JOIN activity_category ac ON ac.category_id = a.category_id
GROUP BY e.region, ac.name
HAVING AVG(p.hours_per_week) > 5
ORDER BY e.region, promedio_horas_semanales DESC;


-- Q2. Ingresos económicos totales por ecoaldea y por tipo de producto
SELECT
    e.name AS ecoaldea,
    pr.product_type,
    SUM(pr.annual_value_clp) AS ingresos_clp,
    COUNT(pr.production_id) AS num_productos,
    ROUND(100.0 * SUM(pr.annual_value_clp) /
        (SELECT SUM(annual_value_clp) FROM production WHERE ecovillage_id = e.ecovillage_id), 1) AS pct_del_total_ecoaldea
FROM ecovillage e
JOIN production pr ON pr.ecovillage_id = e.ecovillage_id
GROUP BY e.ecovillage_id, e.name, pr.product_type
ORDER BY e.name, ingresos_clp DESC;


-- Q3. Miembros más comprometidos (mayor cantidad de horas semanales totales)
SELECT
    e.name AS ecoaldea,
    m.code AS miembro,
    m.age_group,
    r.name AS rol,
    SUM(p.hours_per_week) AS total_horas_semanales,
    COUNT(p.activity_id) AS num_actividades
FROM member m
JOIN ecovillage e ON e.ecovillage_id = m.ecovillage_id
LEFT JOIN role r ON r.role_id = m.role_id
LEFT JOIN participation p ON p.member_id = m.member_id
GROUP BY e.name, m.member_id, m.code, m.age_group, r.name
HAVING SUM(p.hours_per_week) IS NOT NULL
ORDER BY total_horas_semanales DESC
LIMIT 10;


-- Q4. Comparación de modelos de gobernanza vs. tamaño
SELECT
    governance_model,
    COUNT(*) AS num_ecoaldeas,
    ROUND(AVG(hectares)::numeric, 1) AS promedio_hectareas,
    ROUND(AVG(EXTRACT(YEAR FROM CURRENT_DATE) - founded_year)::numeric, 1) AS antiguedad_promedio_anios
FROM ecovillage
GROUP BY governance_model
ORDER BY num_ecoaldeas DESC;


-- Q5. Auto-suficiencia energética: ecoaldeas que producen toda su energía
WITH energia_total AS (
    SELECT
        ecovillage_id,
        SUM(quantity) AS energia_total_kwh,
        SUM(CASE WHEN is_self_produced THEN quantity ELSE 0 END) AS energia_propia_kwh
    FROM resource
    WHERE unit = 'kWh/anio'
    GROUP BY ecovillage_id
)
SELECT
    e.name AS ecoaldea,
    et.energia_total_kwh,
    et.energia_propia_kwh,
    ROUND(100.0 * et.energia_propia_kwh / NULLIF(et.energia_total_kwh, 0), 1) AS pct_autosuficiencia
FROM energia_total et
JOIN ecovillage e ON e.ecovillage_id = et.ecovillage_id
ORDER BY pct_autosuficiencia DESC;
