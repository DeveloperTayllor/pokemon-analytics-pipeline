from .utils_transformation import get_connection

# Objetivo:
#   Criar a tabela de atributos de status (stats) dos pokémons na camada Silver.
#
# Responsabilidade:
#   - Ler o JSON bruto de detalhes dos pokémons
#   - Explodir a estrutura aninhada de stats
#   - Normalizar os dados em formato tabular (1 linha por pokémon + stat)
#   - Persistir os dados em Parquet para uso analítico
#
# Papel na arquitetura:
#   - Normalização de dados semiestruturados
#   - Permite análises por tipo de stat (attack, defense, speed, etc.)
#   - Facilita joins com a tabela silver.pokemon_silver via pokemon_id
#

def create_pokemon_stats_silver():
    # Abre conexão com o DuckDB
    con = get_connection()

    # Cria (ou recria) a tabela Silver normalizada de stats
    con.execute("""
        CREATE OR REPLACE TABLE silver.pokemon_stats_silver AS
        SELECT
            p.id AS pokemon_id,
            s.stat.stat.name AS stat_name,
            s.stat.base_stat AS base_value
        FROM read_json_auto('data/raw/raw_pokeapi_pokemon_details.json') p,
             UNNEST(p.stats) AS s(stat);
    """)

    # Exporta a tabela Silver para Parquet
    # (formato colunar, eficiente para agregações e filtros)
    con.execute("""
        COPY silver.pokemon_stats_silver
        TO 'data/silver/pokemon_stats_silver.parquet'
        (FORMAT PARQUET);
    """)
