import requests as r
from .utils_extract import save_to_raw

list_pokemons = []

# Objetivo:
#   Extrair detalhes de TODOS os pokémons disponíveis na PokeAPI.
#
# Como funciona:
#   - Começa pela URL base do endpoint /pokemon/
#   - Percorre todas as páginas usando o campo "next" (paginação)
#   - Para cada pokémon listado, acessa a URL de detalhe e coleta campos específicos
#
# Saída:
#   - Salva um JSON bruto (raw) com a lista completa de pokémons e seus atributos

def extract_pokemon_details():
    url = "https://pokeapi.co/api/v2/pokemon/"  # Endpoint inicial (primeira página)

    print("Iniciando extração dos pokémons...")

    while url:
        response = r.get(url)
        data = response.json()

        for pokemon in data["results"]:
            pokemon_detail = r.get(pokemon["url"]).json()

            list_pokemons.append({
                "id": pokemon_detail["id"],
                "name": pokemon_detail["name"],
                "height": pokemon_detail["height"],
                "weight": pokemon_detail["weight"],
                "base_experience": pokemon_detail["base_experience"],
                "is_default": pokemon_detail["is_default"],
                "types": pokemon_detail["types"],
                "stats": pokemon_detail["stats"]
            })

        url = data["next"]  # Próxima página (None quando terminar)

    save_to_raw("raw_pokeapi_pokemon_details.json", list_pokemons)
