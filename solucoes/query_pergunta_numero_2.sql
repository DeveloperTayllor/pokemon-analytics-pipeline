-- Aqui eu retorno o numero total de pokémons com mais de uma trilha evolutiva.
SELECT COUNT(*) AS total
FROM (
  SELECT
    from_pokemon
  FROM silver.evolution_silver
  WHERE stage = 1
    AND from_pokemon IS NOT NULL
  GROUP BY from_pokemon
  HAVING COUNT(DISTINCT to_pokemon) > 1
);



--- Aqui eu retorno o nome dos pokémons com mais de uma linha evolutiva
SELECT
  from_pokemon AS pokemon_base,
  COUNT(DISTINCT to_pokemon) AS total_caminhos
FROM silver.evolution_silver
WHERE stage = 1
GROUP BY from_pokemon
HAVING COUNT(DISTINCT to_pokemon) > 1
ORDER BY total_caminhos DESC;

