import requests as r
from utils import save_to_raw

evoluations = []

def extract_evoluations():
    url = "https://pokeapi.co/api/v2/evolution-chain/"

    print("Iniciando extração das evolution chains...")

    while url:
        response = r.get(url)
        data = response.json()

        for item in data["results"]:
            chain_url = item["url"]
            chain_response = r.get(chain_url)
            chain_data = chain_response.json()

            chain_id = chain_data["id"]

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

                    # recursão para próximas evoluções
                    percorrer_chain(evolucao, stage + 1)

            percorrer_chain(chain_data["chain"])

        url = data["next"]

extract_evoluations()

save_to_raw("raw_pokeapi_evolutions.json", evoluations)
