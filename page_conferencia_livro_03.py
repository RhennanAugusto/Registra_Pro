from datetime import datetime, timedelta
import tkinter as tk
import tkinter.messagebox as messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import sqlite3
import os
import datetime
import matplotlib.pyplot as plt

resultado = 0

def criar_banco_dados():
    conn = sqlite3.connect('registro_auxiliar.db')
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

def registrar_producao_diaria(meta_id, data, erros_corrigidos, sem_erros, funcionarios):
    conn = sqlite3.connect('registro_auxiliar.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM producao_diaria WHERE meta_id = ? AND data = ?", (meta_id, data))
    registro_existente = cursor.fetchone()

    if registro_existente:
        cursor.execute("""
            UPDATE producao_diaria
            SET erros_corrigidos = erros_corrigidos + ?, sem_erros = sem_erros + ?, funcionarios = ?
            WHERE meta_id = ? AND data = ?
        """, (erros_corrigidos, sem_erros, funcionarios, meta_id, data))
    else:
        cursor.execute(
            "INSERT INTO producao_diaria (meta_id, data, erros_corrigidos, sem_erros, funcionarios) VALUES (?, ?, ?, ?, ?)",
            (meta_id, data, erros_corrigidos, sem_erros, funcionarios)
        )

    cursor.execute(
        "UPDATE meta SET total_para_conferir = total_para_conferir - ?, total_erros_corrigidos = total_erros_corrigidos + ?, total_sem_erros = total_sem_erros + ? WHERE id = ?",
        (erros_corrigidos + sem_erros, erros_corrigidos, sem_erros, meta_id)
    )

    conn.commit()
    conn.close()

class PageConferenciaLivro03(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Inicializa o banco de dados (garante que as tabelas existem)
        criar_banco_dados()

        back_button = tk.Canvas(self, width=40, height=40)
        back_button.create_polygon(10, 20, 30, 10, 30, 30, fill="black")
        back_button.bind("<Button-1>", lambda e: controller.show_frame("StartPage"))
        back_button.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        label = tk.Label(self, text="Detalhes 3ª CONFERÊNCIA - LIVRO 03 - REGISTRO Auxiliar", font=("Helvetica", 24))
        label.grid(row=1, column=0, columnspan=4, pady=20)

        self.data_label = tk.Label(self, text="Digite a data (AAAA-MM-DD):", font=("Helvetica", 16))
        self.data_label.grid(row=2, column=0, pady=10, padx=10, sticky="e")

        self.data_entry = tk.Entry(self, font=("Helvetica", 16))
        self.data_entry.grid(row=2, column=1, pady=10, padx=10, sticky="w")

        self.ok_button = tk.Button(self, text="OK", font=("Helvetica", 16), command=self.verificar_data)
        self.ok_button.grid(row=2, column=2, pady=10, padx=10, sticky="w")

        self.dados_frame = tk.Frame(self)
        self.dados_frame.grid(row=3, column=0, columnspan=4, padx=20, pady=20, sticky="nsew")

        self.entrada_frame = tk.Frame(self)
        self.entrada_frame.grid(row=4, column=0, columnspan=4, padx=20, pady=20, sticky="nsew")

        self.create_entry_fields()

        self.registrar_button = tk.Button(self.entrada_frame, text="Registrar Produção", font=("Helvetica", 16),
                                          command=self.registrar_transcricoesdef)
        self.registrar_button.grid(row=6, column=1, columnspan=3, pady=20)

        self.proxima_pagina_button = tk.Button(self, text="Relatório Diário", font=("Helvetica", 16), command=self.on_gerar_relatorio_button_click)
        self.proxima_pagina_button.grid(row=5, column=0, columnspan=4, pady=20)

        self.meta_id = 1  # Ajuste conforme necessário

        # Configuração das linhas e colunas da grade
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=3)
        self.grid_rowconfigure(4, weight=3)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.mensagem_label = tk.Label(self, text="", font=("Helvetica", 16))
        self.mensagem_label.grid(row=7, column=0, columnspan=4, pady=10)

    # certo
    def create_entry_fields(self):
        entry_label1 = tk.Label(self.entrada_frame, text="Conferidas com pendencia:", font=("Helvetica", 16))
        entry_label1.grid(row=0, column=0, pady=10, padx=10, sticky="e")
        self.entry1 = tk.Entry(self.entrada_frame, font=("Helvetica", 16))
        self.entry1.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        entry_label2 = tk.Label(self.entrada_frame, text="Conferidas sem pendencia:", font=("Helvetica", 16))
        entry_label2.grid(row=1, column=0, pady=10, padx=10, sticky="e")
        self.entry2 = tk.Entry(self.entrada_frame, font=("Helvetica", 16))
        self.entry2.grid(row=1, column=1, pady=10, padx=10, sticky="w")

        entry_label4 = tk.Label(self.entrada_frame, text="Total funcionários:", font=("Helvetica", 16))
        entry_label4.grid(row=0, column=2, pady=10, padx=10, sticky="e")
        self.entry4 = tk.Entry(self.entrada_frame, font=("Helvetica", 16))
        self.entry4.grid(row=0, column=3, pady=10, padx=10, sticky="w")

    # certo
    def carregar_dados(self, data):
        conn = sqlite3.connect('registro_auxiliar.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM producao_diaria WHERE meta_id = ? AND data = ?", (self.meta_id, data))
        registro = cursor.fetchone()
        conn.close()

        if registro:
            self.entry1.delete(0, tk.END)
            self.entry1.insert(0, registro[3])
            self.entry2.delete(0, tk.END)
            self.entry2.insert(0, registro[4])
            self.entry4.delete(0, tk.END)
            self.entry4.insert(0, registro[5])

    # certo
    def verificar_data(self):
        global resultado
        data = self.data_entry.get()
        if not data:
            messagebox.showerror("Erro", "Por favor, insira uma data válida.")
            return

        conn = sqlite3.connect('registro_auxiliar.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM producao_diaria WHERE data = ?", (data,))
        data_existe = cursor.fetchone()[0]
        conn.close()

        if data_existe:
            self.mensagem_label.config(text="Data já cadastrada, alterações podem ser feitas.", fg="red")
            resultado = 1
            self.carregar_dados(data)
        else:
            self.mensagem_label.config(text="Data não encontrada. Pode continuar o cadastro.", fg="green")
            resultado = 2
            self.entry1.delete(0, tk.END)
            self.entry2.delete(0, tk.END)
            self.entry4.delete(0, tk.END)

    # certo
    def registrar_transcricoesdef(self):
        global resultado
        if resultado == 1:
            data = self.data_entry.get()
            conferidas_com_erros = int(self.entry1.get()) if self.entry1.get() else 0
            conferidas_sem_erros = int(self.entry2.get()) if self.entry2.get() else 0
            funcionarios = int(self.entry4.get()) if self.entry4.get() else 0

            try:
                conn = sqlite3.connect('registro_auxiliar.db')
                cursor = conn.cursor()

                # Configure o tempo limite para aguardar o banco de dados desbloquear
                cursor.execute("PRAGMA busy_timeout = 3000")

                cursor.execute("SELECT COUNT(*) FROM producao_diaria WHERE data = ?", (data,))
                data_existe = cursor.fetchone()[0]

                if data_existe:
                    cursor.execute("""
                                UPDATE producao_diaria 
                                SET erros_corrigidos = ?, sem_erros = ?, funcionarios = ?
                                WHERE data = ?
                            """, (conferidas_com_erros, conferidas_sem_erros, funcionarios, data))
                else:
                    cursor.execute("""
                                INSERT INTO producao_diaria (data, erros_corrigidos, sem_erros, funcionarios) 
                                VALUES (?, ?, ?, ?)
                            """, (data, conferidas_com_erros, conferidas_sem_erros, funcionarios))

                self.atualizar_dados()
                conn.commit()
            except sqlite3.OperationalError as e:
                messagebox.showerror("Erro", f"Erro ao acessar o banco de dados: {e}")
            finally:
                conn.close()
        elif resultado == 2:
            data = self.data_entry.get()

            conferidas_com_erros = int(self.entry1.get()) if self.entry1.get() else 0
            conferidas_sem_erros = int(self.entry2.get()) if self.entry2.get() else 0
            funcionarios = int(self.entry4.get()) if self.entry4.get() else 0

            registrar_producao_diaria(self.meta_id, data, conferidas_com_erros, conferidas_sem_erros, funcionarios)
            self.atualizar_dados()

    #certo
    def atualizar_dados(self):
        for widget in self.dados_frame.winfo_children():
            widget.destroy()

        messagebox.showinfo("Sucesso", "Atualização registrada com sucesso!")

    def on_gerar_relatorio_button_click(self):
        data_atual = self.data_entry.get()
        if not data_atual:
            data_atual = datetime.datetime.now().strftime("%Y-%m-%d")
        self.gerar_relatorio(meta_id=1, data_atual=data_atual)

    def calcular_dias_trabalho(self, meta_id, data_atual):
        conn = sqlite3.connect('registro_auxiliar.db')
        cursor = conn.cursor()

        cursor.execute("SELECT data_inicio FROM meta WHERE id = ?", (meta_id,))
        data_inicio = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT data) FROM producao_diaria WHERE meta_id = ? AND data <= ?", (meta_id, data_atual))
        dias_com_registro = cursor.fetchone()[0]

        conn.close()

        data_inicio_dt = datetime.datetime.strptime(data_inicio, "%d-%m-%Y")
        data_atual_dt = datetime.datetime.strptime(data_atual, "%Y-%m-%d")

        dias_trabalho = self.contar_dias_uteis(data_inicio_dt, data_atual_dt) - 1

        return dias_trabalho, dias_com_registro

    def contar_dias_uteis(self, inicio, fim):
        dias_trabalho = 0
        feriados_br = [
            datetime.date(2024, 1, 1),
            datetime.date(2024, 4, 21),
            datetime.date(2024, 5, 1),
            datetime.date(2024, 9, 7),
            datetime.date(2024, 10, 12),
            datetime.date(2024, 11, 2),
            datetime.date(2024, 11, 15),
            datetime.date(2024, 11, 20),
            datetime.date(2024, 12, 25),
        ]

        dia = inicio
        while dia <= fim:
            if dia.weekday() < 5 and dia not in feriados_br:
                dias_trabalho += 1
            dia += datetime.timedelta(days=1)

        return dias_trabalho

    def gerar_relatorio_progresso(self, meta_id, data_atual):
        relatorio_texto = self.gerar_relatorio(meta_id, data_atual)
        caminho_arquivo_pdf = self.gerar_pdf(relatorio_texto, meta_id)
        caminho_arquivo_imagem = self.gerar_graficos(meta_id, caminho_arquivo_pdf)

        messagebox.showinfo("Relatório Gerado", f"Relatório gerado com sucesso.\nPDF: {caminho_arquivo_pdf}\nImagem do gráfico: {caminho_arquivo_imagem}")

    def prever_termino_servico(self, meta_id, data_atual):
        conn = sqlite3.connect('registro_auxiliar.db')
        cursor = conn.cursor()

        cursor.execute("SELECT total_para_conferir FROM meta WHERE id = ?", (meta_id,))
        total_para_conferir = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(erros_corrigidos + sem_erros) FROM producao_diaria WHERE meta_id = ? AND data <= ?", (meta_id, data_atual))
        total_conferido = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(DISTINCT data) FROM producao_diaria WHERE meta_id = ?", (meta_id,))
        dias_uteis_registrados = cursor.fetchone()[0]

        conn.close()

        if total_conferido == 0 or dias_uteis_registrados == 0:
            return None

        media_diaria = total_conferido / dias_uteis_registrados
        itens_restantes = total_para_conferir - total_conferido
        dias_uteis_restantes = itens_restantes / media_diaria

        data_atual_dt = datetime.datetime.strptime(data_atual, "%Y-%m-%d")
        data_previsao = data_atual_dt
        while dias_uteis_restantes > 0:
            data_previsao += datetime.timedelta(days=1)
            if data_previsao.weekday() < 5:
                dias_uteis_restantes -= 1

        return data_previsao

    def gerar_relatorio(self, meta_id, data_atual):
        conn = sqlite3.connect('registro_auxiliar.db')
        cursor = conn.cursor()

        cursor.execute("SELECT id, total_conferencias, total_para_conferir, total_erros_corrigidos, total_sem_erros, data_inicio FROM meta WHERE id = ?", (meta_id,))
        meta = cursor.fetchone()

        if not meta:
            messagebox.showinfo("Informação", "Nenhuma meta cadastrada.")
            return ""

        cursor.execute("SELECT SUM(erros_corrigidos), SUM(sem_erros) FROM producao_diaria WHERE meta_id = ? AND data <= ?", (meta[0], data_atual))
        total_erros_corrigidos, total_sem_erros = cursor.fetchone() or (0, 0)

        cursor.execute("SELECT COUNT(*), SUM(funcionarios) FROM producao_diaria WHERE meta_id = ? AND data <= ?", (meta[0], data_atual))
        dias_trabalhados, total_funcionarios = cursor.fetchone() or (0, 0)

        cursor.execute("SELECT COUNT(*) FROM producao_diaria WHERE meta_id = ? AND data <= ?", (meta_id, data_atual))
        total_registros = cursor.fetchone()[0]

        media_funcionarios1 = total_funcionarios / total_registros if total_registros > 0 else 0

        para_conferir = 12707
        com_pendencias = 0
        sem_pendencias = 0

        total_conferido = total_erros_corrigidos + total_sem_erros
        
        if meta[1] > 0:
            porcentagem_erros_corrigidos = ((total_erros_corrigidos + com_pendencias) / meta[1]) * 100
            porcentagem_sem_erros = ((total_sem_erros + sem_pendencias) / meta[1]) * 100
            porcentagem_sob_total = ((para_conferir - total_conferido) / meta[1]) * 100
        else:
            messagebox.showerror("Erro", "O Total de conferências não deve ser zero.")
            return ""

        dias_trabalho, dias_com_registro = self.calcular_dias_trabalho(meta_id, data_atual)

        media_producao_funcionario = total_conferido / (media_funcionarios1 * dias_trabalho) if media_funcionarios1 > 0 else 0
        media_producao_diaria = total_conferido / dias_trabalho if dias_trabalho > 0 else 0

        relatorio_texto = (
            f"ID da Meta: {meta[0]}\n"
            f"Período Analisado: {meta[5]} até {data_atual}\n"
            f"Total de conferências: {meta[1]}\n"
            f"Total para conferir: {para_conferir - total_conferido} ({porcentagem_sob_total:.2f}%)\n"
            f"Total conferido com erros e corrigidos: {total_erros_corrigidos + com_pendencias} ({porcentagem_erros_corrigidos:.2f}%)\n"
            f"Total conferido sem erros: {total_sem_erros + sem_pendencias} ({porcentagem_sem_erros:.2f}%)\n"
            f"Total conferido: {total_conferido}\n"
            f"Média de produção por funcionário: {media_producao_funcionario:.2f}\n"
            f"Média de produção diária: {media_producao_diaria:.2f}\n"
        )
        previsao_termino = self.prever_termino_servico(meta[0], data_atual)
        
        if previsao_termino:
            relatorio_texto += f"\nPrevisão de Término: {previsao_termino}\n"

        messagebox.showinfo("Relatório de Conferências", relatorio_texto)
        self.gerar_pdf(relatorio_texto, 1, data_atual)
        caminho_pasta = "T:/Setor Noturno/01. Supervisores/Produtividade/Relatórios/"
        nome_arquivo = f"relatorio_conferencia_REGISTRO_AUXILIAR_{data_atual}.pdf"
        caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)
        self.gerar_graficos(meta_id, caminho_arquivo, data_atual)

        conn.close()
        return relatorio_texto


    #certo
    def gerar_graficos(self, meta_id, caminho_arquivo_pdf, data_atual):
        conn = sqlite3.connect('registro_auxiliar.db')
        cursor = conn.cursor()

        # Consultar dados até a data específica
        cursor.execute(
            "SELECT data, erros_corrigidos, sem_erros FROM producao_diaria WHERE meta_id = ? AND data <= ? ORDER BY data",
            (meta_id, data_atual))
        producao_diaria = cursor.fetchall()

        # Verificar se há dados
        if not producao_diaria:
            messagebox.showinfo("Informação", f"Sem dados até a data: {data_atual}")
            conn.close()
            return ""

        datas = [row[0] for row in producao_diaria]
        erros_corrigidos = [row[1] for row in producao_diaria]
        sem_erros = [row[2] for row in producao_diaria]

        total_erros_corrigidos = sum(erros_corrigidos)
        total_sem_erros = sum(sem_erros)
        total_conferido = total_erros_corrigidos + total_sem_erros

        labels = 'Erros Corrigidos', 'Sem Erros'
        sizes = [total_erros_corrigidos, total_sem_erros]
        explode = (0.1, 0)

        plt.figure(figsize=(15, 5))
        plt.subplot(1, 3, 1)
        plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=140)
        plt.title('Distribuição de Conferências')

        plt.subplot(1, 3, 2)
        plt.plot(datas, erros_corrigidos, label='Erros Corrigidos', marker='o')
        plt.plot(datas, sem_erros, label='Sem Erros', marker='o')
        plt.xlabel('Data')
        plt.ylabel('Quantidade')
        plt.title('Produção Diária')
        plt.legend()

        producao_total = [erros + sem_erro for erros, sem_erro in zip(erros_corrigidos, sem_erros)]
        plt.subplot(1, 3, 3)
        plt.bar(datas, producao_total)
        plt.xlabel('Data')
        plt.ylabel('Produção Total')
        plt.title('Produção Total')

        plt.tight_layout()

        # Salvar imagem em um local específico
        caminho_pasta = "T:/Setor Noturno/01. Supervisores/Produtividade/Relatórios/"
        nome_arquivo_imagem = f'grafico_REGISTRO_AUXILIAR_{data_atual}.png'
        caminho_arquivo_imagem = os.path.join(caminho_pasta, nome_arquivo_imagem)
        plt.savefig(caminho_arquivo_imagem)

        plt.close()  # Fechar o plot para liberar recursos

        conn.close()
        return caminho_arquivo_imagem
    # certo
    
    def gerar_pdf(self, texto, meta_id, data_atual):
        caminho_pasta = "T:/Setor Noturno/01. Supervisores/Produtividade/Relatórios/"
        caminho_arquivo = os.path.join(caminho_pasta,
                                       f"relatorio_conferencia_REGISTRO_AUXILIAR_{data_atual}.pdf")
        c = canvas.Canvas(caminho_arquivo, pagesize=letter)
        width, height = letter
        c.drawString(100, height - 40, "Relatório de Progresso")

        y = height - 60
        for linha in texto.split("\n"):
            c.drawString(40, y, linha)
            y -= 20
        c.save()

        return caminho_arquivo
# Exemplo de uso

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Cadastro de Metas e Produção Diária")
    root.geometry("800x600")

    main_frame = PageConferenciaLivro03(root, None)
    main_frame.pack(fill="both", expand=True)

    root.mainloop()
