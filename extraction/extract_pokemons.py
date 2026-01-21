import requests as r
from utils import save_to_raw


pokemons = []

def extract_pokemon_details():
    url = "https://pokeapi.co/api/v2/pokemon/"

    print("Iniciando extração dos pokemons...")

    while url:
        response = r.get(url)
        data = response.json()

        for item in data["results"]:
            detalhe = r.get(item["url"]).json()

            pokemons.append({
                "id": detalhe["id"],
                "name": detalhe["name"],
                "height": detalhe["height"],
                "weight": detalhe["weight"],
                "base_experience": detalhe["base_experience"],
                "is_default": detalhe["is_default"],
                "types": detalhe["types"],
                "stats": detalhe["stats"]
            })
        url = data["next"]

extract_pokemon_details()

save_to_raw("raw_pokeapi_pokemon_details.json", pokemons)