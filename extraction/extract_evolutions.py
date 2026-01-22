import requests as r
from .utils_extract import save_to_raw

evoluations = []

# Objetivo:
#   Extrair TODOS os caminhos evolutivos (evolution chains) disponíveis na PokeAPI.
#
# Como funciona:
#   - Lê o endpoint /evolution-chain/ que é paginado
#   - Para cada item retornado, acessa a URL de detalhe da chain (1 request por chain)
#   - O payload de detalhe vem em formato de árvore (nested JSON)
#   - A função recursiva "percorrer_chain" percorre essa árvore e transforma em registros flat:
#       from_pokemon -> to_pokemon, com chain_id e stage (nível da evolução)
#
# Saída:
#   - Salva um JSON bruto (raw) com as relações de evolução em formato tabular (flat)
#
def extract_evolutions():
    url = "https://pokeapi.co/api/v2/evolution-chain/"  # Endpoint inicial (primeira página)

    print("Iniciando extração das evolution chains...")

    while url:
        response = r.get(url)
        data = response.json()

        for item in data["results"]:
            chain_url = item["url"]
            chain_response = r.get(chain_url)
            chain_data = chain_response.json()

            chain_id = chain_data["id"]

            # Percorre a estrutura em árvore (chain -> evolves_to -> evolves_to...)
            # e gera registros do tipo: base -> evolução1, evolução1 -> evolução2, etc.
            def percorrer_chain(no, stage=1):
                from_name = no["species"]["name"]

                for evolucao in no["evolves_to"]:
                    to_name = evolucao["species"]["name"]

                    evoluations.append({
                        "chain_id": chain_id,
                        "from_pokemon": from_name,
                        "to_pokemon": to_name,
                        "stage": stage
                    })

                    # Recursão: continua descendo na árvore para capturar evoluções futuras
                    percorrer_chain(evolucao, stage + 1)

            percorrer_chain(chain_data["chain"])

        url = data["next"]  # Próxima página (None quando terminar)

    save_to_raw("raw_pokeapi_evolutions.json", evoluations)
