from .utils_transformation import get_connection

# Objetivo:
#   Criar a tabela de pokémons na camada Silver a partir dos dados brutos (Raw).
#
# Responsabilidade:
#   - Ler o JSON bruto com detalhes dos pokémons
#   - Selecionar e padronizar os campos relevantes
#   - Criar a tabela no schema Silver
#   - Persistir os dados em formato Parquet
#
# Papel na arquitetura:
#   - Conversão de dados semiestruturados (JSON) para dados estruturados
#   - Base principal para análises, joins e modelagem dimensional no Gold
#   - Fonte de verdade para atributos básicos do pokémon
#

def create_pokemon_silver():
    # Abre conexão com o DuckDB
    con = get_connection()

    # Garante a existência do schema Silver
    con.execute("CREATE SCHEMA IF NOT EXISTS silver;")

    # Cria (ou recria) a tabela Silver de pokémons
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

    # Exporta a tabela Silver para Parquet
    # (formato colunar, otimizado para leitura analítica)
    con.execute("""
        COPY silver.pokemon_silver
        TO 'data/silver/pokemon_silver.parquet'
        (FORMAT PARQUET);
    """)
