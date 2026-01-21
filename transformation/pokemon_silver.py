from utils import get_connection

def create_pokemon_silver():
    con = get_connection()
    con.execute("CREATE SCHEMA IF NOT EXISTS silver;")

    con.execute("""
        CREATE OR REPLACE TABLE silver.pokemon_silver AS
        SELECT
            id AS pokemon_id,
            name,
            height,
            weight,
            base_experience,
            is_default
        FROM read_json_auto('data/raw/raw_pokeapi_pokemon_details.json')
    """)

    con.execute("""
        COPY silver.pokemon_silver
        TO 'data/silver/pokemon_silver.parquet'
        (FORMAT PARQUET);
    """)