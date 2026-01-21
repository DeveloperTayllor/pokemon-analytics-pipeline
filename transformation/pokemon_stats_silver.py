from utils import get_connection

def create_pokemon_stats_silver():
    con = get_connection()

    con.execute("""
    CREATE OR REPLACE TABLE silver.pokemon_stats_silver AS
    SELECT
        p.id AS pokemon_id,
        s.stat.stat.name AS stat_name,
        s.stat.base_stat AS base_value
    FROM read_json_auto('data/raw/raw_pokeapi_pokemon_details.json') p,
         UNNEST(p.stats) AS s(stat);
    """)

    con.execute("""
    COPY silver.pokemon_stats_silver
    TO 'data/silver/pokemon_stats_silver.parquet'
    (FORMAT PARQUET);
""")
