import json
import os

def save_to_raw(nome_arquivo: str, dados: list | dict):
    os.makedirs("data/raw", exist_ok=True)

    caminho = os.path.join("data/raw", nome_arquivo)

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    print(f"Arquivo salvo em: {caminho}")