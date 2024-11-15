import psycopg2

def get_user_confirmation():
    while True:
        response = input('Deseja confirmar a alteração? (s/n): ').strip().lower()
        if response == 's':
            return True
        elif response == 'n':
            return False
        else:
            print("Resposta inválida. Por favor, digite 's' para sim ou 'n' para não.")

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

def realizar_transacao():
    try:
        dsn = "dbname=teste user=postgres password=12345 host=localhost port=3000"
        conn = psycopg2.connect(dsn)

        conn.autocommit = False  # Controle de transação manual
        cursor = conn.cursor()

        user_id = escolher_usuario(cursor)

        # Obter o limite de crédito inicial do usuário
        cursor.execute("SELECT limite_de_credito FROM users WHERE id = %s;", (user_id,))
        limite_inicial = cursor.fetchone()[0]
        print(f"Limite de crédito inicial do usuário (ID {user_id}): {limite_inicial}")

        # Solicitar o novo limite de crédito
        novo_limite = float(input("Digite o novo limite de crédito: ").strip())

        print("\nIniciando a transação...")

        # Executar o update condicional
        cursor.execute("""
            UPDATE users
            SET limite_de_credito = %s
            WHERE id = %s AND limite_de_credito = %s;
        """, (novo_limite, user_id, limite_inicial))

        # Verificar se o update foi bem-sucedido
        if cursor.rowcount == 0:
            print("Alteração cancelada: o limite de crédito foi modificado por outra transação.")
            conn.rollback()  # Reverter a transação
        else:
            # Obter confirmação do usuário
            if get_user_confirmation():
                conn.commit()  # Confirmar a transação
                print("Alteração confirmada e salva.")
            else:
                conn.rollback()  # Reverter a transação
                print("Alteração cancelada.")

        cursor.close()
        conn.close()

    except Exception as e:
        print("Ocorreu um erro:", e)
        if conn:
            conn.rollback()
        if conn:
            conn.close()

# Chamar a função para executar o sistema
realizar_transacao()
