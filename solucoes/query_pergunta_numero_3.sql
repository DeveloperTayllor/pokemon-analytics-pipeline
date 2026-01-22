SELECT
  p.name,
  p.base_experience,
  STRING_AGG(t.type_name, ', ') AS types
FROM silver.pokemon_silver p
JOIN silver.pokemon_types_silver t
  ON p.pokemon_id = t.pokemon_id
WHERE p.is_default = true
  AND p.pokemon_id IN (
    SELECT pokemon_id
    FROM silver.pokemon_types_silver
    WHERE type_name = 'ice'
  )
GROUP BY p.name, p.base_experience
ORDER BY p.base_experience DESC
LIMIT 10;