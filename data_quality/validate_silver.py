import pandas as pd
import great_expectations as ge
from pathlib import Path

SILVER_PATH = Path("data/silver")

FILES = {
    "pokemon": "pokemon_silver.parquet",
    "types": "pokemon_types_silver.parquet",
    "stats": "pokemon_stats_silver.parquet",
    "evolution": "evolutions.parquet",
}


def validate_pokemon(df):
    gdf = ge.from_pandas(df)
    checks = [
        gdf.expect_column_values_to_not_be_null("pokemon_id"),
        gdf.expect_column_values_to_be_unique("pokemon_id"),
    ]
    return all(c["success"] for c in checks)


def validate_types(df):
    gdf = ge.from_pandas(df)
    checks = [
        gdf.expect_column_values_to_not_be_null("pokemon_id"),
        gdf.expect_column_values_to_not_be_null("type_name"),
        gdf.expect_column_values_to_be_in_set("slot", [1, 2]),
    ]
    return all(c["success"] for c in checks)


def validate_stats(df):
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
    gdf = ge.from_pandas(df)
    checks = [
        gdf.expect_column_values_to_not_be_null("chain_id"),
        gdf.expect_column_values_to_not_be_null("from_pokemon"),
        gdf.expect_column_values_to_not_be_null("to_pokemon"),
    ]
    return all(c["success"] for c in checks)


VALIDATORS = {
    "pokemon": validate_pokemon,
    "types": validate_types,
    "stats": validate_stats,
    "evolution": validate_evolution,
}


def run():
    failures = []

    for name, file in FILES.items():
        path = SILVER_PATH / file
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")

        df = pd.read_parquet(path)
        ok = VALIDATORS[name](df)

        if ok:
            print(f"✅ {file} OK")
        else:
            print(f"❌ {file} FALHOU")
            failures.append(file)

    if failures:
        raise RuntimeError(f"Data Quality falhou: {failures}")

    print("✅ Data Quality passou para toda a camada Silver")


if __name__ == "__main__":
    run()
