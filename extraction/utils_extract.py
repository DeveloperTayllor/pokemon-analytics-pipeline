import json
import os

# Objetivo:
#   Persistir dados brutos (raw) em formato JSON na camada Raw do projeto.
#
# Responsabilidade:
#   - Garantir que o diretório data/raw exista
#   - Salvar o conteúdo recebido sem transformação ou enriquecimento
#   - Padronizar o local e o formato dos arquivos da camada Raw
#
# Parâmetros:
#   nome_arquivo (str): Nome do arquivo a ser salvo (ex: raw_pokeapi_pokemon.json)
#   dados (list | dict): Dados brutos extraídos da fonte de origem
#
# Papel na arquitetura:
#   - Função utilitária compartilhada por todos os extratores
#   - Garante consistência e previsibilidade na camada Raw
#
# Observações:
#   - Nenhuma regra de negócio é aplicada aqui
#   - Qualquer validação ou modelagem deve ocorrer nas camadas Silver/Gold

def save_to_raw(nome_arquivo: str, dados: list | dict):
    # Cria o diretório da camada Raw caso ainda não exista
    os.makedirs("data/raw", exist_ok=True)

    # Caminho completo do arquivo dentro da camada Raw
    caminho = os.path.join("data/raw", nome_arquivo)

    # Escrita do arquivo JSON preservando caracteres e identação para leitura humana
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    print(f"Arquivo salvo em: {caminho}")
