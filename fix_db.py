# fix_db.py
import sqlite3
import os

# Encontra o caminho para o arquivo do banco de dados
db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')

try:
    # Conecta ao banco de dados
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Comando SQL para deletar o registro problemático
    # Ele deleta todos os registros de migração do app 'pedidos'
    sql_command = "DELETE FROM django_migrations WHERE app = 'pedidos';"

    # Executa o comando
    cursor.execute(sql_command)

    # Salva (comita) as alterações no banco de dados
    conn.commit()

    print("\n✅ Registro da migração de 'pedidos' removido com sucesso do banco de dados!")

except sqlite3.Error as e:
    print(f"\n❌ Ocorreu um erro: {e}")

finally:
    # Fecha a conexão
    if conn:
        conn.close()