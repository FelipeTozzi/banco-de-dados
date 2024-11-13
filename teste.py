import psycopg2

try:
    print("Tentando conectar ao banco de dados...")
    conn = psycopg2.connect(
        dbname="teste",
        user="postgre",
        password="12345",
        host="localhost",
        port="3000"  # Certifique-se de que isso seja uma string e não em bytes
    )
    print("Conexão bem-sucedida!")
    conn.close()

except psycopg2.OperationalError as op_error:
    print("Erro operacional ao conectar ao banco de dados:", op_error)
except Exception as e:
    print("Erro geral ao conectar ao banco de dados:", e)
