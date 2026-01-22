from .pokemon_silver import create_pokemon_silver
from .pokemon_stats_silver import create_pokemon_stats_silver
from .pokemon_types_silver import create_pokemon_types_silver
from .evolutions_silver import create_evolutions_silver

# Objetivo:
#   Orquestrar a criação de todas as tabelas da camada Silver no DuckDB.
#
# Responsabilidade:
#   - Executar as transformações Raw -> Silver
#   - Garantir que todas as tabelas Silver sejam criadas de forma consistente
#   - Centralizar o fluxo de transformação em um único ponto de entrada
#
# Papel na arquitetura:
#   - Entry point da camada Silver
#   - Facilita a orquestração futura com Prefect, Airflow ou execução via CLI
#   - Define a ordem de criação das tabelas Silver
#
# Observações:
#   - As transformações são estruturais (JSON -> tabelas normalizadas)
#   - Cada função é responsável por criar e persistir sua própria tabela
#   - Não há dependência direta entre as tabelas nesta camada

def run_transformation_to_silver():
    create_pokemon_silver()
    create_pokemon_stats_silver()
    create_pokemon_types_silver()
    create_evolutions_silver()
