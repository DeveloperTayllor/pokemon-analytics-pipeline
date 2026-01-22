import pandas as pd
import great_expectations as ge
from pathlib import Path

# Caminho padrão onde os arquivos Parquet da camada Silver são gerados
SILVER_PATH = Path("data/silver")

# Mapeamento lógico (dataset) -> nome do arquivo na camada Silver
FILES = {
    "pokemon": "pokemon_silver.parquet",
    "types": "pokemon_types_silver.parquet",
    "stats": "pokemon_stats_silver.parquet",
    "evolution": "evolutions.parquet",
}

# --------------------------------------------------------------------------------------
# VALIDAÇÕES POR DATASET
#
# Estratégia:
#   - Cada função abaixo valida um dataset específico da Silver.
#   - As validações são regras simples, diretas e fáceis de defender:
#       * campos obrigatórios não nulos
#       * chaves únicas quando aplicável
#       * domínios controlados (ex: slot 1/2, nomes de stats)
#       * limites plausíveis (ex: base_value entre 1 e 255)
#
# Objetivo dessas validações:
#   - Atuar como "quality gate" antes do consumo analítico / criação da camada Gold.
#   - Quebrar o pipeline cedo caso a Silver esteja inconsistente.
# --------------------------------------------------------------------------------------

def validate_pokemon(df):
    # Validações básicas de integridade para a tabela principal de pokémons
    gdf = ge.from_pandas(df)
    checks = [
        gdf.expect_column_values_to_not_be_null("pokemon_id"),
        gdf.expect_column_values_to_be_unique("pokemon_id"),
    ]
    return all(c["success"] for c in checks)


def validate_types(df):
    # Validações para a tabela normalizada de tipos
    gdf = ge.from_pandas(df)
    checks = [
        gdf.expect_column_values_to_not_be_null("pokemon_id"),
        gdf.expect_column_values_to_not_be_null("type_name"),
        gdf.expect_column_values_to_be_in_set("slot", [1, 2]),  # 1 = tipo primário, 2 = secundário
    ]
    return all(c["success"] for c in checks)


def validate_stats(df):
    # Validações para a tabela normalizada de stats
    gdf = ge.from_pandas(df)
    checks = [
        gdf.expect_column_values_to_not_be_null("pokemon_id"),
        gdf.expect_column_values_to_not_be_null("stat_name"),
        gdf.expect_column_values_to_be_in_set(
            "stat_name",
            ["hp", "attack", "defense", "special-attack", "special-defense", "speed"]
        ),
        gdf.expect_column_values_to_be_between("base_value", min_value=1, max_value=255),
    ]
    return all(c["success"] for c in checks)


def validate_evolution(df):
    # Validações para a tabela de relações evolutivas
    gdf = ge.from_pandas(df)
    checks = [
        gdf.expect_column_values_to_not_be_null("chain_id"),
        gdf.expect_column_values_to_not_be_null("from_pokemon"),
        gdf.expect_column_values_to_not_be_null("to_pokemon"),
    ]
    return all(c["success"] for c in checks)


# Registro dos validadores: facilita escalar (adicionar novos datasets e regras)
VALIDATORS = {
    "pokemon": validate_pokemon,
    "types": validate_types,
    "stats": validate_stats,
    "evolution": validate_evolution,
}

# --------------------------------------------------------------------------------------
# ORQUESTRAÇÃO DAS VALIDAÇÕES
#
# Objetivo:
#   - Ler todos os arquivos Parquet da Silver
#   - Rodar o validador correspondente
#   - Exibir status no console (OK/FALHOU)
#   - Falhar o processo se qualquer dataset estiver inválido (gate de qualidade)
# --------------------------------------------------------------------------------------

def run():
    failures = []

    for name, file in FILES.items():
        path = SILVER_PATH / file

        # Falha rápida: se o arquivo não existe, não faz sentido continuar
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")

        # Leitura do Parquet e execução das regras de qualidade
        df = pd.read_parquet(path)
        ok = VALIDATORS[name](df)

        if ok:
            print(f"✅ {file} OK")
        else:
            print(f"❌ {file} FALHOU")
            failures.append(file)

    # Se qualquer dataset falhar, quebra o pipeline com erro explícito
    if failures:
        raise RuntimeError(f"Data Quality falhou: {failures}")

    print("✅ Data Quality passou para toda a camada Silver")


# Permite execução local via terminal: python <arquivo>.py
if __name__ == "__main__":
    run()
