from transformation.transformation_main import run_transformation_to_silver
from extraction.extraction_main import extract_data_to_raw



def main():
    print("=== PIPELINE START ===")

    # 1) EXTRAÇÃO (opcional)
    print("-> EXTRACTION")
    extract_data_to_raw()

    # 2) TRANSFORMAÇÃO (SILVER)
    print("-> TRANSFORMATION (SILVER)")
    run_transformation_to_silver()

    # 3) QUALIDADE (GREAT EXPECTATIONS)
    #print("-> DATA QUALITY (GE)")
    #run_quality()

    print("=== PIPELINE FINISH ===")


if __name__ == "__main__":
    main()