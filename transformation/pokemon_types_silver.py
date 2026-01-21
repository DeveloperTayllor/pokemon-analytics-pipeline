from utils import get_connection

def create_pokemon_types_silver():
    con = get_connection()

    con.execute("""
        CREATE OR REPLACE TABLE silver.pokemon_types_silver AS
        SELECT
            p.id                AS pokemon_id,
            t.type.type.name    AS type_name,
            t.type.slot         AS slot
        FROM read_json_auto('data/raw/raw_pokeapi_pokemon_details.json') p,
             UNNEST(p.types) AS t(type);
    """)

    con.execute("""
    COPY silver.pokemon_types_silver
    TO 'data/silver/pokemon_types_silver.parquet'
    (FORMAT PARQUET);
""")
