import os
import psycopg2

def get_connection():
    # Ajuste a senha abaixo (ou defina a variavel de ambiente DB_PASSWORD)
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", 5432)),
        database=os.environ.get("DB_NAME", "estoque_notebooks"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "estoque")
    )
    return conn
