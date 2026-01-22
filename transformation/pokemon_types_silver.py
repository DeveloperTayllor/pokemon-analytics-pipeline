from .utils_transformation import get_connection

# Objetivo:
#   Criar a tabela de tipos (types) dos pokémons na camada Silver.
#
# Responsabilidade:
#   - Ler o JSON bruto de detalhes dos pokémons
#   - Explodir a estrutura aninhada de tipos
#   - Normalizar os dados em formato tabular
#   - Persistir os dados em Parquet
#
# Papel na arquitetura:
#   - Normalização de dados semiestruturados
#   - Permite análises por tipo (fire, water, grass, etc.)
#   - Suporta filtros, agregações e joins com a tabela de pokémons
#

def create_pokemon_types_silver():
    # Abre conexão com o DuckDB
    con = get_connection()

    # Cria (ou recria) a tabela Silver normalizada de tipos
    con.execute("""
        CREATE OR REPLACE TABLE silver.pokemon_types_silver AS
        SELECT
            p.id                AS pokemon_id,
            t.type.type.name    AS type_name,
            t.type.slot         AS slot
        FROM read_json_auto('data/raw/raw_pokeapi_pokemon_details.json') p,
             UNNEST(p.types) AS t(type);
    """)

    # Exporta a tabela Silver para Parquet
    # (formato colunar, otimizado para consultas analíticas)
    con.execute("""
        COPY silver.pokemon_types_silver
        TO 'data/silver/pokemon_types_silver.parquet'
        (FORMAT PARQUET);
    """)
