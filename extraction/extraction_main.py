from .extract_evolutions import extract_evolutions
from .extract_pokemons import extract_pokemon_details

# Objetivo:
#   Centralizar e orquestrar a extração dos dados da PokeAPI para a camada Raw.
#
# Responsabilidade:
#   - Disparar a extração dos dados de pokémons (endpoint /pokemon)
#   - Disparar a extração das cadeias evolutivas (endpoint /evolution-chain)
#
# Papel na arquitetura:
#   - Atua como ponto único de entrada da camada de extração
#   - Facilita a orquestração futura (Prefect, Airflow, CLI, etc.)
#   - Garante que todos os datasets necessários para a Raw sejam gerados juntos
#
# Observações:
#   - A ordem de execução é sequencial
#   - Cada função é responsável por salvar seus próprios arquivos na camada Raw

def extract_data_to_raw():
    extract_pokemon_details()
    extract_evolutions()
