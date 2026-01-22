import duckdb

# Objetivo:
#   Centralizar a criação da conexão com o banco DuckDB do projeto.
#
# Responsabilidade:
#   - Abrir conexão com o arquivo de banco de dados DuckDB
#   - Padronizar o acesso ao banco em toda a aplicação
#
# Papel na arquitetura:
#   - Função utilitária compartilhada por todas as camadas de transformação
#   - Evita duplicação de código e inconsistências de conexão
#


def get_connection():
    return duckdb.connect("pokemon.duckdb")
