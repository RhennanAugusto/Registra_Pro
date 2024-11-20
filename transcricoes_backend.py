import sqlite3
import datetime


def criar_banco_dados():
    conn = sqlite3.connect('transcricoes.db')
    cursor = conn.cursor()

    cursor.execute('''
          CREATE TABLE IF NOT EXISTS metas (
              id INTEGER PRIMARY KEY AUTOINCREMENT, 
              total_transcricoes INTEGER,
              total_para_digitar INTEGER,
              total_para_conferir INTEGER,
              total_para_cadastrar INTEGER,
              total_ja_cadastrado INTEGER,  -- Adicione esta coluna
              total_digitado INTEGER,
              total_conferido INTEGER,
              total_cadastrado INTEGER,
              data_inicio TEXT
          )
      ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transcricoes_diarias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            digitadas INTEGER,
            conferidas INTEGER,
            cadastradas INTEGER,
            meta_id INTEGER,
            funcionarios_digitando INTEGER,
            funcionarios_conferindo INTEGER,
            funcionarios_cadastrando INTEGER,
            FOREIGN KEY(meta_id) REFERENCES metas(id)
        )
    ''')
    conn.commit()
    conn.close()

def cadastrar_meta(total_transcricoes, total_para_digitar, total_para_conferir, total_para_cadastrar, data_inicio):
    total_digitado = 0
    total_conferido = 0
    total_cadastrado = 0

    conn = sqlite3.connect('transcricoes.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO metas (total_transcricoes, total_para_digitar, total_para_conferir, total_para_cadastrar, total_digitado, total_conferido, total_cadastrado, data_inicio) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (total_transcricoes, total_para_digitar, total_para_conferir, total_para_cadastrar, total_digitado, total_conferido, total_cadastrado, data_inicio))
    conn.commit()
    conn.close()

    #print("Meta cadastrada com sucesso!")

def registrar_transcricoes_diarias(data, digitadas, conferidas, cadastradas, meta_id, funcionarios_digitando,
                                   funcionarios_conferindo, funcionarios_cadastrando):

            conn = sqlite3.connect('transcricoes.db', timeout=10)  # Aumentar o timeout para 10 segundos
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE metas SET total_para_conferir = total_para_conferir + ?, total_para_digitar = total_para_digitar - ? WHERE id = ?",
                (digitadas, digitadas, meta_id))

            cursor.execute(
                "UPDATE metas SET total_digitado = total_digitado + ?, total_conferido = total_conferido + ?, total_cadastrado = total_cadastrado + ? WHERE id = ?",
                (digitadas, conferidas, cadastradas, meta_id))

            cursor.execute(
                "INSERT INTO transcricoes_diarias (data, digitadas, conferidas, cadastradas, meta_id, funcionarios_digitando, funcionarios_conferindo, funcionarios_cadastrando) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (data, digitadas, conferidas, cadastradas, meta_id, funcionarios_digitando, funcionarios_conferindo,
                 funcionarios_cadastrando))

            conn.commit()
            conn.close()

            #print("Transcrições diárias registradas com sucesso!")


def obter_dados_producao(meta_id):
    conn = sqlite3.connect('transcricoes.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT total_digitado, total_conferido, total_cadastrado FROM metas WHERE id = ?
    ''', (meta_id,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return {
            "total_digitado": result[0],
            "total_conferido": result[1],
            "total_cadastrado": result[2]
        }
    else:
        return None
