-- ============================================================================
-- ECOALDEAS CHILENAS — Queries básicas (nivel 1)
-- ============================================================================
-- Demuestra: SELECT, WHERE, ORDER BY, LIMIT, agregaciones simples, JOINs básicos
-- ============================================================================


-- Q1. Listar todas las ecoaldeas con su antigüedad en años
SELECT
    name AS ecoaldea,
    region,
    founded_year,
    (EXTRACT(YEAR FROM CURRENT_DATE) - founded_year) AS antiguedad_anios,
    hectares
FROM ecovillage
ORDER BY founded_year ASC;


-- Q2. Cantidad de miembros por ecoaldea
SELECT
    e.name AS ecoaldea,
    e.region,
    COUNT(m.member_id) AS total_miembros,
    SUM(CASE WHEN m.is_founder THEN 1 ELSE 0 END) AS fundadores,
    SUM(CASE WHEN m.residency_type = 'permanente' THEN 1 ELSE 0 END) AS permanentes
FROM ecovillage e
LEFT JOIN member m ON m.ecovillage_id = e.ecovillage_id
GROUP BY e.ecovillage_id, e.name, e.region
ORDER BY total_miembros DESC;


-- Q3. Distribución de miembros por grupo etario
SELECT
    age_group,
    COUNT(*) AS total,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM member), 1) AS porcentaje
FROM member
GROUP BY age_group
ORDER BY age_group;


-- Q4. Ecoaldeas más grandes en hectáreas
SELECT
    name,
    region,
    hectares,
    governance_model
FROM ecovillage
ORDER BY hectares DESC
LIMIT 3;


-- Q5. Listado de actividades por categoría
SELECT
    ac.name AS categoria,
    COUNT(a.activity_id) AS num_actividades_distintas,
    COUNT(DISTINCT a.ecovillage_id) AS ecoaldeas_que_la_practican
FROM activity_category ac
LEFT JOIN activity a ON a.category_id = ac.category_id
GROUP BY ac.category_id, ac.name
ORDER BY num_actividades_distintas DESC;
