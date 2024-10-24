import schedule
import time
import sqlite3
from datetime import datetime

# Conectar ou criar o banco de dados SQLite
def init_db():
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            data_hora TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Adicionar uma tarefa no banco de dados
def agendar_tarefa(descricao, data_hora):
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tarefas (descricao, data_hora) VALUES (?, ?)', (descricao, data_hora))
    conn.commit()
    conn.close()
    print(f"Tarefa agendada: {descricao} em {data_hora}")

# Listar todas as tarefas
def listar_tarefas():
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tarefas')
    tarefas = cursor.fetchall()
    conn.close()
    return tarefas

# Excluir uma tarefa
def excluir_tarefa(tarefa_id):
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tarefas WHERE id = ?', (tarefa_id,))
    conn.commit()
    conn.close()
    print(f"Tarefa {tarefa_id} excluída.")

# Executar uma tarefa
def executar_tarefa(tarefa):
    print(f"Executando tarefa: {tarefa[1]} às {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    excluir_tarefa(tarefa[0])

# Agendar a execução das tarefas
def agendar_execucao():
    tarefas = listar_tarefas()
    for tarefa in tarefas:
        descricao, data_hora = tarefa[1], tarefa[2]
        data_hora_obj = datetime.strptime(data_hora, '%Y-%m-%d %H:%M:%S')
        if datetime.now() < data_hora_obj:
            delay = (data_hora_obj - datetime.now()).total_seconds()
            schedule.every(delay).seconds.do(executar_tarefa, tarefa)

# Função principal para rodar o scheduler
def rodar_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    init_db()

    # Exemplos de uso
    agendar_tarefa("Enviar relatório", "2024-10-15 15:00:00")
    agendar_tarefa("Reunião com cliente", "2024-10-16 10:00:00")

    print("Tarefas agendadas:")
    for tarefa in listar_tarefas():
        print(tarefa)

    agendar_execucao()
    rodar_scheduler()

