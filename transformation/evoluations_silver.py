from utils import get_connection

def create_evoluations_silver():
    con = get_connection()
    con.execute("CREATE SCHEMA IF NOT EXISTS silver;")

    con.execute("""
    CREATE OR REPLACE TABLE silver.evolution_silver AS
    SELECT
        chain_id,
        from_pokemon,
        to_pokemon,
        stage
    FROM read_json_auto('data/raw/raw_pokeapi_evolutions.json');
    """)

    con.execute("""
    COPY silver.evolution_silver
    TO 'data/silver/evolutions.parquet'
    (FORMAT PARQUET);
    """)