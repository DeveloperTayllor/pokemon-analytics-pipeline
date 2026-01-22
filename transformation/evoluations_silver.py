from .utils_transformation import get_connection

# Objetivo:
#   Criar a tabela de evoluções na camada Silver a partir dos dados brutos (Raw).
#
# Responsabilidade:
#   - Ler o JSON bruto de evolution chains
#   - Estruturar os dados em formato tabular
#   - Persistir a tabela no schema Silver
#   - Exportar os dados em formato Parquet para consumo analítico
#
# Papel na arquitetura:
#   - Primeira camada de transformação (Raw -> Silver)
#   - Remove o formato semiestruturado (JSON)
#   - Gera dados prontos para consultas SQL e modelagem no Gold
#


def create_evoluations_silver():
    # Abre conexão com o DuckDB
    con = get_connection()

    # Garante a existência do schema Silver
    con.execute("CREATE SCHEMA IF NOT EXISTS silver;")

    # Cria (ou recria) a tabela Silver a partir do JSON bruto
    con.execute("""
        CREATE OR REPLACE TABLE silver.evolution_silver AS
        SELECT
            chain_id,
            from_pokemon,
            to_pokemon,
            stage
        FROM read_json_auto('data/raw/raw_pokeapi_evolutions.json');
    """)

    # Exporta a tabela Silver para Parquet
    # (formato colunar, ideal para analytics e camadas posteriores)
    con.execute("""
        COPY silver.evolution_silver
        TO 'data/silver/evolutions.parquet'
        (FORMAT PARQUET);
    """)
