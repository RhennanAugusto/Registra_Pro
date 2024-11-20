import tkinter as tk
import sqlite3
from datetime import datetime


class CadastroDeMetasRegistroGeral(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        back_button = tk.Canvas(self, width=40, height=40)
        back_button.create_polygon(10, 20, 30, 10, 30, 30, fill="black")
        back_button.bind("<Button-1>", lambda e: controller.show_frame("StartPage"))
        back_button.pack(anchor="nw", padx=10, pady=10)

        label = tk.Label(self, text="Cadastro de meta: 3ª CONFERÊNCIA - LIVRO 02 - REGISTRO GERAL",
                         font=("Helvetica", 24))
        label.pack(pady=20)

        entry_label1 = tk.Label(self, text="Total de 3ª CONFERÊNCIA - REGISTRO GERAL:", font=("Helvetica", 16))
        entry_label1.pack(pady=10)
        self.entry1 = tk.Entry(self, font=("Helvetica", 16))
        self.entry1.pack()

        entry_label2 = tk.Label(self, text="Total para conferir:", font=("Helvetica", 16))
        entry_label2.pack(pady=10)
        self.entry2 = tk.Entry(self, font=("Helvetica", 16))
        self.entry2.pack()

        entry_label3 = tk.Label(self, text="Total de conferidas com erros identificados e corrigidos:",
                                font=("Helvetica", 16))
        entry_label3.pack(pady=10)
        self.entry3 = tk.Entry(self, font=("Helvetica", 16))
        self.entry3.pack()

        entry_label4 = tk.Label(self, text="Total de conferidas sem erros identificados:", font=("Helvetica", 16))
        entry_label4.pack(pady=10)
        self.entry4 = tk.Entry(self, font=("Helvetica", 16))
        self.entry4.pack()

        entry_label6 = tk.Label(self, text="Data de início (DD-MM-AAAA):", font=("Helvetica", 16))
        entry_label6.pack(pady=10)
        self.entry6 = tk.Entry(self, font=("Helvetica", 16))
        self.entry6.pack()

        ok_button = tk.Button(self, text="OK", font=("Helvetica", 16), command=self.submit_values)
        ok_button.pack(pady=20)


        self.add_footer()
        self.criar_banco_dados()

    def submit_values(self):
        value1 = self.entry1.get()
        value2 = self.entry2.get()
        value3 = self.entry3.get()
        value4 = self.entry4.get()
        value6 = self.entry6.get()

        # Chama a função cadastrar_meta com os valores obtidos
        self.meta_id = cadastrar_meta(
            int(value1),
            int(value2),
            int(value3),
            int(value4),
            value6
        )

        # Opcional: Limpar os campos após submeter os valores
        self.entry1.delete(0, tk.END)
        self.entry2.delete(0, tk.END)
        self.entry3.delete(0, tk.END)
        self.entry4.delete(0, tk.END)
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

    def criar_banco_dados(self):
        conn = sqlite3.connect('conferencias.db')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS meta (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            total_conferencias INTEGER,
                            total_para_conferir INTEGER,
                            total_erros_corrigidos INTEGER,
                            total_sem_erros INTEGER,
                            data_inicio DATE
                        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS producao_diaria (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            meta_id INTEGER,
                            data DATE,
                            erros_corrigidos INTEGER,
                            sem_erros INTEGER,
                            funcionarios INTEGER,
                            FOREIGN KEY (meta_id) REFERENCES meta (id)
                        )''')

        conn.commit()
        conn.close()

    def registrar_producao_diaria(self):
        # Obter valores de produção diária (precisa adaptar para pegar os valores corretamente)
        self.erros_corrigidos = int(self.entry3.get())
        self.sem_erros = int(self.entry4.get())
        self.funcionarios = 5  # Exemplo, você precisa adaptar para pegar este valor de alguma forma
        data = datetime.today().date()

        conn = sqlite3.connect('conferencias.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO producao_diaria (meta_id, data, erros_corrigidos, sem_erros, funcionarios) VALUES (?, ?, ?, ?, ?)",
            (self.meta_id, data, self.erros_corrigidos, self.sem_erros, self.funcionarios))

        cursor.execute(
            "UPDATE meta SET total_para_conferir = total_para_conferir - ?, total_erros_corrigidos = total_erros_corrigidos + ?, total_sem_erros = total_sem_erros + ? WHERE id = ?",
            (self.erros_corrigidos + self.sem_erros, self.erros_corrigidos, self.sem_erros, self.meta_id))

        conn.commit()
        conn.close()
        #print("Produção diária registrada com sucesso!")


def cadastrar_meta(total_conferencias, total_para_conferir, total_erros_corrigidos, total_sem_erros, data_inicio):
    conn = sqlite3.connect('conferencias.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO meta (total_conferencias, total_para_conferir, total_erros_corrigidos, total_sem_erros, data_inicio) VALUES (?, ?, ?, ?, ?)",
        (total_conferencias, total_para_conferir, total_erros_corrigidos, total_sem_erros, data_inicio))
    conn.commit()
    meta_id = cursor.lastrowid
    conn.close()
    #print("Meta cadastrada com sucesso!")
    return meta_id
