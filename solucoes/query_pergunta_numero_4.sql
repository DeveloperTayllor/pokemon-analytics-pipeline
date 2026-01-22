WITH deltas AS (
  SELECT
    e.from_pokemon AS pre_evolution,
    e.to_pokemon   AS evolution,
    s1.stat_name,
    (s2.base_value - s1.base_value) AS stat_increase
  FROM silver.evolution_silver e
  JOIN silver.pokemon_silver p1
    ON lower(p1.name) = lower(e.from_pokemon)
  JOIN silver.pokemon_silver p2
    ON lower(p2.name) = lower(e.to_pokemon)
  JOIN silver.pokemon_stats_silver s1
    ON s1.pokemon_id = p1.pokemon_id
  JOIN silver.pokemon_stats_silver s2
    ON s2.pokemon_id = p2.pokemon_id
   AND s2.stat_name = s1.stat_name
),
max_per_evo AS (
  SELECT
    pre_evolution,
    evolution,
    MAX(stat_increase) AS max_increase
  FROM deltas
  GROUP BY pre_evolution, evolution
)
SELECT
  d.pre_evolution,
  d.evolution,
  d.stat_name,
  d.stat_increase
FROM deltas d
JOIN max_per_evo m
  ON d.pre_evolution = m.pre_evolution
 AND d.evolution     = m.evolution
 AND d.stat_increase = m.max_increase
ORDER BY d.stat_increase DESC
LIMIT 7;