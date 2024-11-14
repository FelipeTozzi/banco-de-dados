import psycopg2
from psycopg2 import sql

# Função para obter a confirmação do usuário
def get_user_confirmation():
    while True:
        response = input('Deseja confirmar a alteração? (s/n): ').strip().lower()
        if response == 's':
            return True
        elif response == 'n':
            return False
        else:
            print("Resposta inválida. Por favor, digite 's' para sim ou 'n' para não.")

# Função para exibir todos os usuários e permitir a seleção de um usuário pelo ID
def escolher_usuario(cursor):
    cursor.execute("SELECT id, name, limite_de_credito FROM users;")
    users = cursor.fetchall()

    print("\nLista de usuários:")
    for user in users:
        print(f"ID: {user[0]}, Nome: {user[1]}, Limite de Crédito: {user[2]}")

    while True:
        try:
            user_id = int(input("\nDigite o ID do usuário que deseja alterar o limite de crédito: ").strip())
            if any(user[0] == user_id for user in users):
                return user_id
            else:
                print("ID inválido. Por favor, escolha um ID da lista.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")

# Função principal para realizar a transação
def realizar_transacao():
    # Conectar ao banco de dados
    try:
        dsn = "dbname=teste user=postgres password=12345 host=172.18.199.237 port=3000"
        conn = psycopg2.connect(dsn)

        # Ativar o autocommit no início para evitar problemas de sessão
        conn.autocommit = True
        cursor = conn.cursor()

        # Exibir lista de usuários e permitir a escolha do usuário a ser atualizado
        user_id = escolher_usuario(cursor)

        cursor.execute("""
            START TRANSACTION
        """)

        # Solicitar o novo valor de limite de crédito
        novo_limite = float(input("Digite o novo limite de crédito: ").strip())

        # Iniciar a transação desativando o autocommit
        conn.autocommit = True
        print("\nIniciando a transação...")

        # Executar o update
        
        cursor.execute("""
            UPDATE users
            SET limite_de_credito = %s
            WHERE id = %s;
        """, (novo_limite, user_id))

        # Obter confirmação do usuário
        if get_user_confirmation():
            # Confirmar a transação (COMMIT)
            conn.commit()
            print("Alteração confirmada e salva.")
            cursor.execute(""" COMMIT """)
        else:
            # Reverter a transação (ROLLBACK)
            conn.rollback()
            print("Alteração cancelada.")

        # Fechar o cursor e a conexão
        cursor.close()
        conn.close()

    except Exception as e:
        print("Ocorreu um erro:", e)
        # Se houver erro, faz rollback e fecha a conexão
        if conn:
            conn.rollback()
        if conn:
            conn.close()

# Chamar a função para executar o sistema
realizar_transacao()