from transformation.transformation_main import run_transformation_to_silver
from extraction.extraction_main import extract_data_to_raw
from data_quality.validate_silver import run as run_data_quality




def main():
    print("=== PIPELINE START ===")

    # 1) EXTRAÇÃO (opcional)
    print("-> EXTRACTION")
    extract_data_to_raw()

    # 2) TRANSFORMAÇÃO (SILVER)
    print("-> TRANSFORMATION (SILVER)")
    run_transformation_to_silver()

    # 3) QUALIDADE (GREAT EXPECTATIONS)
    print("🧪 Validação de Qualidade (Silver)")
    run_data_quality()

    print("✅ Pipeline finalizado com sucesso")



if __name__ == "__main__":
    main()