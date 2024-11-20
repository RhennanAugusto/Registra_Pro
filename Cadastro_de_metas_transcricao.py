import tkinter as tk
import sqlite3
from datetime import datetime
total_digitar = 0
total_conferir = 0 # Inicialmente, nenhuma transcrição foi conferida
total_cadastrar = 0
class CadastroDeMetasTranscricao(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        back_button = tk.Canvas(self, width=40, height=40)
        back_button.create_polygon(10, 20, 30, 10, 30, 30, fill="black")
        back_button.bind("<Button-1>", lambda e: controller.show_frame("StartPage"))
        back_button.pack(anchor="nw", padx=10, pady=10)

        label = tk.Label(self, text="Cadastro de meta: TRANSCRIÇÃO DAS TRANSMISSÕES", font=("Helvetica", 24))
        label.pack(pady=20)

        entry_label1 = tk.Label(self, text="Total de transcrições:", font=("Helvetica", 16))
        entry_label1.pack(pady=10)
        self.entry1 = tk.Entry(self, font=("Helvetica", 16))
        self.entry1.pack()

        entry_label2 = tk.Label(self, text="Total de transcrições para digitar:", font=("Helvetica", 16))
        entry_label2.pack(pady=10)
        self.entry2 = tk.Entry(self, font=("Helvetica", 16))
        self.entry2.pack()

        entry_label3 = tk.Label(self, text="Total de transcrições para conferir:", font=("Helvetica", 16))
        entry_label3.pack(pady=10)
        self.entry3 = tk.Entry(self, font=("Helvetica", 16))
        self.entry3.pack()

        entry_label4 = tk.Label(self, text="Total de transcrições para cadastrar:", font=("Helvetica", 16))
        entry_label4.pack(pady=10)
        self.entry4 = tk.Entry(self, font=("Helvetica", 16))
        self.entry4.pack()

        entry_label5 = tk.Label(self, text="Total de transcrições já cadastradas:", font=("Helvetica", 16))
        entry_label5.pack(pady=10)
        self.entry5 = tk.Entry(self, font=("Helvetica", 16))
        self.entry5.pack()

        entry_label6 = tk.Label(self, text="Data de início (DD-MM-AAAA):", font=("Helvetica", 16))
        entry_label6.pack(pady=10)
        self.entry6 = tk.Entry(self, font=("Helvetica", 16))
        self.entry6.pack()

        ok_button = tk.Button(self, text="OK", font=("Helvetica", 16), command=self.submit_values)
        ok_button.pack(pady=20)

        self.add_footer()

    def submit_values(self):
        value1 = self.entry1.get()
        value2 = self.entry2.get()
        value3 = self.entry3.get()
        value4 = self.entry4.get()
        value5 = self.entry5.get()
        value6 = self.entry6.get()

        global total_digitar, total_conferir, total_cadastrar
        total_digitar = int(value2)
        total_conferir = int(value3)
        total_cadastrar = int(value4)

        # Chama a função cadastrar_meta com os valores obtidos
        cadastrar_meta(
            int(value1),
            int(value2),
            int(value3),
            int(value4),
            int(value5),
            value6
        )

        # Opcional: Limpar os campos após submeter os valores
        self.entry1.delete(0, tk.END)
        self.entry2.delete(0, tk.END)
        self.entry3.delete(0, tk.END)
        self.entry4.delete(0, tk.END)
        self.entry5.delete(0, tk.END)
        self.entry6.delete(0, tk.END)

    def add_footer(self):
        footer_frame = tk.Frame(self)
        footer_frame.pack(side=tk.BOTTOM, pady=10)

        phrase1 = tk.Label(footer_frame, text="V.1.0.0", font=("Helvetica", 12))
        phrase1.pack(side=tk.LEFT, padx=5)

        separator1 = tk.Label(footer_frame, text="|", font=("Helvetica", 12))
        separator1.pack(side=tk.LEFT, padx=5)

        phrase2 = tk.Label(footer_frame, text="Cartório do 1º Ofício de Notas e Registro de Imóveis",
                           font=("Helvetica", 12))
        phrase2.pack(side=tk.LEFT, padx=5)

        separator2 = tk.Label(footer_frame, text="|", font=("Helvetica", 12))
        separator2.pack(side=tk.LEFT, padx=5)

        current_date = datetime.now().strftime("%d/%m/%Y")
        date_label = tk.Label(footer_frame, text=current_date, font=("Helvetica", 12))
        date_label.pack(side=tk.LEFT, padx=5)

import sqlite3

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

def cadastrar_meta(total_transcricoes, total_para_digitar, total_para_conferir, total_para_cadastrar,
                       total_ja_cadastrado, data_inicio):
        total_digitado = 0  # Inicialmente, nenhuma transcrição foi digitada
        total_conferido = 0  # Inicialmente, nenhuma transcrição foi conferida
        total_cadastrado = 0  # Inicialmente, nenhuma transcrição foi cadastrada

        conn = sqlite3.connect('transcricoes.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO metas (total_transcricoes, total_para_digitar, total_para_conferir, total_para_cadastrar, total_ja_cadastrado, total_digitado, total_conferido, total_cadastrado, data_inicio) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (total_transcricoes, total_para_digitar, total_para_conferir, total_para_cadastrar, total_ja_cadastrado,
             total_digitado, total_conferido, total_cadastrado, data_inicio))
        conn.commit()
        conn.close()

        #print("Meta cadastrada com sucesso!")
