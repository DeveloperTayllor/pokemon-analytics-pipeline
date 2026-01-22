SELECT
    name,
    height * 0.1 AS height_metros,
    weight * 0.1 AS weight_kg
FROM silver.pokemon_silver
WHERE is_default = true
ORDER BY height_metros DESC
LIMIT 10;
