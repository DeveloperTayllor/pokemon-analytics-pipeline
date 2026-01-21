from .pokemon_silver import create_pokemon_silver
from .pokemon_stats_silver import create_pokemon_stats_silver
from .pokemon_types_silver import create_pokemon_types_silver
from .evoluations_silver import create_evoluations_silver


def run_transformation_to_silver():
    create_pokemon_silver()
    create_pokemon_stats_silver()
    create_pokemon_types_silver()
    create_evoluations_silver()


