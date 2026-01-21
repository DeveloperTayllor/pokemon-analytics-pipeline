from .extract_evoluations import extract_evoluations
from .extract_pokemons import extract_pokemon_details


def extract_data_to_raw():
    extract_pokemon_details()
    extract_evoluations()


