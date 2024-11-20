from datetime import datetime
from transcricoes_backend import criar_banco_dados, registrar_transcricoes_diarias
import tkinter as tk
import tkinter.messagebox as messagebox
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import sqlite3
import matplotlib.pyplot as plt
import os
#from Cadastro_de_metas_transcricao import total_conferir, total_digitar, total_cadastrar

resultado = 0
class PageProducaoDetalhes(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.criar_banco_dados()

        back_button = tk.Canvas(self, width=40, height=40)
        back_button.create_polygon(10, 20, 30, 10, 30, 30, fill="black")
        back_button.bind("<Button-1>", lambda e: controller.show_frame("StartPage"))
        back_button.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        label = tk.Label(self, text="Detalhes da TRANSCRIÇÃO DAS TRANSMISSÕES", font=("Helvetica", 24))
        label.grid(row=1, column=0, columnspan=4, pady=20)

        self.data_label = tk.Label(self, text="Digite a data (AAAA-MM-DD):", font=("Helvetica", 16))
        self.data_label.grid(row=2, column=0, pady=10, padx=10, sticky="e")

        self.data_entry = tk.Entry(self, font=("Helvetica", 16))
        self.data_entry.grid(row=2, column=1, pady=10, padx=10, sticky="w")

        self.ok_button = tk.Button(self, text="OK", font=("Helvetica", 16), command=self.verificar_data)
        self.ok_button.grid(row=2, column=2, pady=10, padx=10, sticky="w")

        self.mensagem_label = tk.Label(self, text="", font=("Helvetica", 16))
        self.mensagem_label.grid(row=3, column=0, columnspan=4, pady=10)

        self.dados_frame = tk.Frame(self)
        self.dados_frame.grid(row=4, column=0, columnspan=4, padx=20, pady=20, sticky="nsew")

        self.entrada_frame = tk.Frame(self)
        self.entrada_frame.grid(row=5, column=0, columnspan=4, padx=20, pady=20, sticky="nsew")

        self.create_entry_fields()

        self.registrar_button = tk.Button(self.entrada_frame, text="Registrar Produção ", font=("Helvetica", 16), command=self.registrar_transcricoesdef)
        self.registrar_button.grid(row=6, column=1, columnspan=3, pady=20)

        self.proxima_pagina_button = tk.Button(self, text="Relatório Diário", font=("Helvetica", 16), command=self.on_gerar_relatorio_button_click)
        self.proxima_pagina_button.grid(row=7, column=0, columnspan=4, pady=20)

        self.meta_id = 1

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=3)
        self.grid_rowconfigure(6, weight=3)
        self.grid_rowconfigure(7, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

    def criar_banco_dados(self):
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

    def create_entry_fields(self):
        entry_label1 = tk.Label(self.entrada_frame, text="Transcrições digitadas:", font=("Helvetica", 16))
        entry_label1.grid(row=0, column=0, pady=10, padx=10, sticky="e")
        self.entry1 = tk.Entry(self.entrada_frame, font=("Helvetica", 16))
        self.entry1.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        entry_label2 = tk.Label(self.entrada_frame, text="Transcrições conferidas:", font=("Helvetica", 16))
        entry_label2.grid(row=1, column=0, pady=10, padx=10, sticky="e")
        self.entry2 = tk.Entry(self.entrada_frame, font=("Helvetica", 16))
        self.entry2.grid(row=1, column=1, pady=10, padx=10, sticky="w")

        entry_label3 = tk.Label(self.entrada_frame, text="Transcrições completas:", font=("Helvetica", 16))
        entry_label3.grid(row=2, column=0, pady=10, padx=10, sticky="e")
        self.entry3 = tk.Entry(self.entrada_frame, font=("Helvetica", 16))
        self.entry3.grid(row=2, column=1, pady=10, padx=10, sticky="w")

        entry_label4 = tk.Label(self.entrada_frame, text="Total funcionários digitação:", font=("Helvetica", 16))
        entry_label4.grid(row=0, column=2, pady=10, padx=10, sticky="e")
        self.entry4 = tk.Entry(self.entrada_frame, font=("Helvetica", 16))
        self.entry4.grid(row=0, column=3, pady=10, padx=10, sticky="w")

        entry_label5 = tk.Label(self.entrada_frame, text="Total funcionários conferência:", font=("Helvetica", 16))
        entry_label5.grid(row=1, column=2, pady=10, padx=10, sticky="e")
        self.entry5 = tk.Entry(self.entrada_frame, font=("Helvetica", 16))
        self.entry5.grid(row=1, column=3, pady=10, padx=10, sticky="w")

        entry_label6 = tk.Label(self.entrada_frame, text="Total funcionários cadastro de transcrições completas:", font=("Helvetica", 16))
        entry_label6.grid(row=2, column=2, pady=10, padx=10, sticky="e")
        self.entry6 = tk.Entry(self.entrada_frame, font=("Helvetica", 16))
        self.entry6.grid(row=2, column=3, pady=10, padx=10, sticky="w")

    def verificar_data(self):
        global resultado
        data = self.data_entry.get()
        if not data:
            messagebox.showerror("Erro", "Por favor, insira uma data válida.")
            return

        conn = sqlite3.connect('transcricoes.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM transcricoes_diarias WHERE data = ?", (data,))
        data_existe = cursor.fetchone()[0]
        conn.close()

        if data_existe:
            self.mensagem_label.config(text="Data já cadastrada, alterações podem ser feitas!.", fg="red")
            resultado = 1
            self.carregar_dados(data)
        else:
            self.mensagem_label.config(text="Data não encontrada. Pode continuar o cadastro.", fg="green")
            resultado = 2
            self.entry1.delete(0, tk.END)
            self.entry2.delete(0, tk.END)
            self.entry3.delete(0, tk.END)
            self.entry4.delete(0, tk.END)
            self.entry5.delete(0, tk.END)
            self.entry6.delete(0, tk.END)
            

    def carregar_dados(self, data):
        conn = sqlite3.connect('transcricoes.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transcricoes_diarias WHERE data = ?", (data,))
        registro = cursor.fetchone()
        conn.close()

        if registro:
            self.entry1.delete(0, tk.END)
            self.entry1.insert(0, registro[2])
            self.entry2.delete(0, tk.END)
            self.entry2.insert(0, registro[3])
            self.entry3.delete(0, tk.END)
            self.entry3.insert(0, registro[4])
            self.entry4.delete(0, tk.END)
            self.entry4.insert(0, registro[6])
            self.entry5.delete(0, tk.END)
            self.entry5.insert(0, registro[7])
            self.entry6.delete(0, tk.END)
            self.entry6.insert(0, registro[8])


    def registrar_transcricoes1(self):
        data = self.data_entry.get()
        digitadas = int(self.entry1.get())
        conferidas = int(self.entry2.get())
        cadastradas = int(self.entry3.get())
        funcionarios_digitacao = int(self.entry4.get())
        funcionarios_conferencia = int(self.entry5.get())
        funcionarios_cadastro = int(self.entry6.get())

        conn = sqlite3.connect('transcricoes.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM transcricoes_diarias WHERE data = ?", (data,))
        data_existe = cursor.fetchone()[0]

        if data_existe:
            cursor.execute("""
                UPDATE transcricoes_diarias 
                SET digitadas = ?, conferidas = ?, cadastradas = ?, funcionarios_digitando = ?, funcionarios_conferindo = ?, funcionarios_cadastrando = ?
                WHERE data = ?
            """, (digitadas, conferidas, cadastradas, funcionarios_digitacao, funcionarios_conferencia, funcionarios_cadastro, data))
        else:
            cursor.execute("""
                INSERT INTO transcricoes_diarias (data, digitadas, conferidas, cadastradas, funcionarios_digitando, funcionarios_conferindo, funcionarios_cadastrando) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (data, digitadas, conferidas, cadastradas, funcionarios_digitacao, funcionarios_conferencia, funcionarios_cadastro))

        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Atualização registrada com sucesso!")

    def registrar_transcricoesdef(self):
        global resultado
        if resultado == 1:
            self.registrar_transcricoes1()
        elif resultado == 2:
            self.registrar_transcricoes2()

    def registrar_transcricoes2(self):
        data = self.data_entry.get()
        digitadas = int(self.entry1.get()) if self.entry1.get() else 0
        conferidas = int(self.entry2.get()) if self.entry2.get() else 0
        cadastradas = int(self.entry3.get()) if self.entry3.get() else 0
        funcionarios_digitando = int(self.entry4.get()) if self.entry4.get() else 0
        funcionarios_conferindo = int(self.entry5.get()) if self.entry5.get() else 0
        funcionarios_cadastrando = int(self.entry6.get()) if self.entry6.get() else 0

        registrar_transcricoes_diarias(data, digitadas, conferidas, cadastradas, self.meta_id,
                                       funcionarios_digitando, funcionarios_conferindo, funcionarios_cadastrando)
        self.atualizar_dados()

    def atualizar_dados(self):
        for widget in self.dados_frame.winfo_children():
            widget.destroy()

        messagebox.showinfo("Sucesso", "Dados registrados com sucesso!")

    def on_gerar_relatorio_button_click(self):
        # Supondo que a data digitada pelo usuário esteja em self.data_entry
        data_atual = self.data_entry.get()
        if not data_atual:
            # Se a data atual não for fornecida, use a data de hoje
            data_atual = datetime.datetime.now().strftime("%Y-%m-%d")
        self.gerar_relatorio_progresso(meta_id=1, data_atual=data_atual)

    def calcular_dias_trabalho(self, meta_id, data_atual):
        conn = sqlite3.connect('transcricoes.db')
        cursor = conn.cursor()

        cursor.execute("SELECT data_inicio FROM metas WHERE id = ?", (meta_id,))
        data_inicio = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT data) FROM transcricoes_diarias WHERE meta_id = ?", (meta_id,))
        dias_com_registro = cursor.fetchone()[0]

        conn.close()

        data_inicio_dt = datetime.datetime.strptime(data_inicio, "%d-%m-%Y")  # Ajuste o formato conforme necessário
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
        conn = sqlite3.connect('transcricoes.db')
        conn.row_factory = sqlite3.Row  # Configura o row_factory para retornar dicionários
        cursor = conn.cursor()

        cursor.execute(
            "SELECT total_transcricoes, total_para_digitar, total_para_conferir, total_para_cadastrar, total_digitado, total_conferido, total_cadastrado, data_inicio FROM metas WHERE id = ?",
            (meta_id,))
        meta = cursor.fetchone()

        cursor.execute(
            "SELECT SUM(digitadas), SUM(conferidas), SUM(cadastradas), SUM(funcionarios_digitando), SUM(funcionarios_conferindo), SUM(funcionarios_cadastrando) FROM transcricoes_diarias WHERE meta_id = ? AND data <= ?",
            (meta_id, data_atual))
        total_digitadas, total_conferidas, total_cadastradas, total_func_digitando, total_func_conferindo, total_func_cadastrando = cursor.fetchone()

        cursor.execute("SELECT COUNT(*) FROM transcricoes_diarias WHERE meta_id = ? AND data <= ?", (meta_id, data_atual))
        total_registros = cursor.fetchone()[0]

        # Calcula as médias dos funcionários com base nos valores atualizados
        media_funcionarios1 = total_func_digitando / total_registros if total_registros > 0 else 0
        media_funcionarios2 = total_func_conferindo / total_registros if total_registros > 0 else 0
        media_funcionarios3 = total_func_cadastrando / total_registros if total_registros > 0 else 0



        #Ajuste tecnico, arrumar dps!!!!
        total_digitar = 16312   
        total_conferir = 8898
        total_cadastrar = 4360
        total_completas = 426

        total_restante_digitado = total_digitar - total_digitadas
        total_restante_conferido = total_conferir + total_digitadas - total_conferidas
        total_restante_cadastrado = total_cadastrar + total_conferidas - total_cadastradas

        if total_digitar != 0:
            total_restante_digitado = total_digitar - total_digitadas
            percentual_digitado = (total_digitadas / total_digitar) * 100
        else:
            total_restante_digitado = total_digitar
            percentual_digitado = 0.0

        # Verifica se total_conferir é diferente de zero antes de calcular o percentual
        if total_conferir != 0:
            total_restante_conferido = total_conferir + total_digitadas - total_conferidas
            if total_restante_conferido != 0:
                percentual_conferido = (total_conferidas / total_restante_conferido) * 100
            else:
                percentual_conferido = 0  # Ou outro valor padrão/ação apropriada
        else:
            total_restante_conferido = 0
            percentual_conferido = 0 

        # Verifica se total_cadastrar é diferente de zero antes de calcular o percentual
        if total_cadastrar != 0:
            total_restante_cadastrado = total_cadastrar + total_conferidas - total_cadastradas
            if total_restante_cadastrado != 0 :
                percentual_cadastrado = (total_cadastradas / total_restante_cadastrado) * 100
            else:
                percentual_cadastrado = 0
        else:
            total_restante_cadastrado = total_cadastrar
            percentual_cadastrado = 0.0

        dias_trabalho, dias_com_registro = self.calcular_dias_trabalho(meta_id, data_atual)

        media_digitacao = total_digitadas / (media_funcionarios1 * dias_trabalho) if media_funcionarios1 > 0 else 0
        media_conferencia = total_conferidas / (media_funcionarios2 * dias_trabalho) if media_funcionarios2 > 0 else 0
        media_cadastro = total_cadastradas / (media_funcionarios3  * dias_trabalho) if media_funcionarios3 > 0 else 0

        

        media_total_digitacao = total_digitadas / dias_trabalho if dias_com_registro > 0 else 0
        media_total_conferencia = total_conferidas / dias_trabalho if dias_com_registro > 0 else 0
        media_total_cadastro = total_cadastradas / dias_trabalho if dias_com_registro > 0 else 0

        data_hoje_str = self.data_entry.get()

        relatorio_texto = ""
        relatorio_texto += "\nRelatório de Progresso Detalhado:\n"
        relatorio_texto += f"Período Analisado: {meta['data_inicio']} até {data_hoje_str} \n"
        relatorio_texto += f"\nTotal de transcrições: {meta['total_transcricoes']}\n"
        relatorio_texto += f"Total de transcrições para digitar: {total_restante_digitado}\n"
        relatorio_texto += f"Total de transcrições para conferir: {total_restante_conferido}\n"
        relatorio_texto += f"Total de transcrições para cadastrar: {total_restante_cadastrado}\n"
        relatorio_texto += f"Transcrições Digitadas:\n"
        relatorio_texto += f"  Total digitado: {total_digitadas} ({percentual_digitado:.2f}% em relação ao total cadastrado)\n"
        relatorio_texto += f"  Total restante: {total_restante_digitado} ({(total_restante_digitado / meta['total_transcricoes'] * 100):.2f}%)\n"
        relatorio_texto += f"  Média por funcionário por dia: {media_digitacao:.2f}\n"
        relatorio_texto += f"  Média total por dia: {media_total_digitacao:.2f}\n\n"
        relatorio_texto += f"Transcrições Conferidas:\n"
        relatorio_texto += f"  Total conferido: {total_conferidas} ({percentual_conferido:.2f}% em relação ao total restante)\n"
        relatorio_texto += f"  Total restante: {total_restante_conferido} ({(total_restante_conferido / meta['total_transcricoes'] * 100):.2f}%)\n"
        relatorio_texto += f"  Média por funcionário por dia: {media_conferencia:.2f}\n"
        relatorio_texto += f"  Média total por dia: {media_total_conferencia:.2f}\n\n"
        relatorio_texto += f"Transcrições Cadastradas:\n"
        relatorio_texto += f"  Total cadastrado: {total_cadastradas} ({percentual_cadastrado:.2f}% em relação ao total restante)\n"
        relatorio_texto += f"  Total restante: {total_restante_cadastrado} ({(total_restante_cadastrado / meta['total_transcricoes'] * 100):.2f}%)\n"
        relatorio_texto += f"  Média por funcionário por dia: {media_cadastro:.2f}\n"
        relatorio_texto += f"  Média total por dia: {media_total_cadastro:.2f}\n"
        relatorio_texto += f"\nTotal de Transcrições Completas: {total_cadastradas + total_completas} ({((total_cadastradas + total_completas) / meta['total_transcricoes'] * 100):.2f}%)\n"

        # Adicionando a previsão de conclusão das metas
        if total_restante_digitado > 0:
            dias_restantes = total_restante_digitado / media_total_digitacao if media_total_digitacao > 0 else float(
                'inf')
            previsao_conclusao = datetime.datetime.now() + datetime.timedelta(days=dias_restantes)
            relatorio_texto += f"\nPrevisão de conclusão das metas de digitação: {previsao_conclusao.strftime('%Y-%m-%d')}\n"

        if total_restante_conferido > 0:
            dias_restantes = total_restante_conferido / media_total_conferencia if media_total_conferencia > 0 else float(
                'inf')
            previsao_conclusao = datetime.datetime.now() + datetime.timedelta(days=dias_restantes)
            relatorio_texto += f"Previsão de conclusão das metas de conferência: {previsao_conclusao.strftime('%Y-%m-%d')}\n"

        if total_restante_cadastrado > 0:
            dias_restantes = total_restante_cadastrado / media_total_cadastro if media_total_cadastro > 0 else float(
                'inf')
            if media_total_cadastro > 0:
                previsao_conclusao = datetime.datetime.now() + datetime.timedelta(days=dias_restantes)
                relatorio_texto += f"Previsão de conclusão das metas de cadastramento: {previsao_conclusao.strftime('%Y-%m-%d')}\n"
            else:
                relatorio_texto += "Sem previsões de término por enquanto das metas de cadastro\n"

        messagebox.showinfo("Relatório de Progresso", relatorio_texto)

        nome_arquivo = f"Relatorio_transcrições_{data_hoje_str}.pdf"
        diretorio_destino = "T:/Setor Noturno/01. Supervisores/Produtividade/Relatórios/"

        if not os.path.exists(diretorio_destino):
            os.makedirs(diretorio_destino)

        caminho_completo = os.path.join(diretorio_destino, nome_arquivo)

        caminho_imagem = os.path.join(diretorio_destino, f"grafico_transcricoes_{data_hoje_str}.png")

        self.gerar_pdf(relatorio_texto, caminho_completo)

        self.gerar_graficos_progresso(meta_id, total_func_digitando, total_func_conferindo, total_func_cadastrando, total_digitadas, total_conferidas, total_cadastradas, media_digitacao,
                                  media_conferencia, media_cadastro, media_total_digitacao, media_total_conferencia,
                                  media_total_cadastro, caminho_imagem, data_atual)
        conn.close()

    def gerar_graficos_progresso(self, meta_id, total_func_digitando, total_func_conferindo, total_func_cadastrando, total_digitadas, total_conferidas, total_cadastradas, media_digitacao,
                                  media_conferencia, media_cadastro, media_total_digitacao, media_total_conferencia,
                                  media_total_cadastro, caminho_imagem, data_atual):
        conn = sqlite3.connect('transcricoes.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT data, digitadas, conferidas, cadastradas, funcionarios_digitando, funcionarios_conferindo, funcionarios_cadastrando FROM transcricoes_diarias WHERE meta_id = ? AND data <= ?",
            (meta_id, data_atual))
        dados_diarios = cursor.fetchall()

        cursor.execute(
            "SELECT total_para_digitar, total_para_conferir, total_para_cadastrar, total_digitado, total_conferido, total_cadastrado FROM metas WHERE id = ?",
            (meta_id,))
        meta = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) FROM transcricoes_diarias WHERE meta_id = ? AND data <= ?", (meta_id, data_atual))
        total_registros = cursor.fetchone()[0]
        
        # Calcula as médias dos funcionários
        media_funcionarios1 = total_func_digitando / total_registros if total_registros > 0 else 0
        media_funcionarios2 = total_func_conferindo / total_registros if total_registros > 0 else 0
        media_funcionarios3 = total_func_cadastrando / total_registros if total_registros > 0 else 0

        conn.close()

        datas = [row[0] for row in dados_diarios]
        digitadas = [row[1] for row in dados_diarios]
        conferidas = [row[2] for row in dados_diarios]
        cadastradas = [row[3] for row in dados_diarios]

        total_digitado = sum(digitadas)
        total_conferido = sum(conferidas)
        total_cadastrado = sum(cadastradas)

        total_func_digitando = sum(row[4] for row in dados_diarios)
        total_func_conferindo = sum(row[5] for row in dados_diarios)
        total_func_cadastrando = sum(row[6] for row in dados_diarios)

        dias_trabalho, dias_com_registro = self.calcular_dias_trabalho(meta_id, data_atual)
        
        medias_funcionarios = [
            total_digitado / (media_funcionarios1 * dias_trabalho) if media_funcionarios1 > 0 else 0,
            total_conferido / (media_funcionarios2 * dias_trabalho) if media_funcionarios2> 0 else 0,
            total_cadastrado / (media_funcionarios3 * dias_trabalho) if media_funcionarios3 > 0 else 0,
        ]

        fig, axs = plt.subplots(2, 2, figsize=(14, 10))

        axs[0, 0].pie([total_digitado, total_conferido, total_cadastrado],
                      labels=['Digitado', 'Conferido', 'Cadastrado'], autopct='%1.1f%%', startangle=140)
        axs[0, 0].set_title('Distribuição de Transcrições por Área')

        axs[0, 1].plot(datas, digitadas, label='Digitadas', marker='o')
        axs[0, 1].plot(datas, conferidas, label='Conferidas', marker='o')
        axs[0, 1].plot(datas, cadastradas, label='Cadastradas', marker='o')
        axs[0, 1].set_xlabel('Data')
        axs[0, 1].set_ylabel('Quantidade')
        axs[0, 1].set_title('Produção Diária por Área')
        axs[0, 1].legend()
        axs[0, 1].grid(True)
        axs[0, 1].tick_params(axis='x', rotation=45)

        medias_diarias = [total_digitado / dias_trabalho, total_conferido / dias_trabalho,
                          total_cadastrado / dias_trabalho]
        axs[1, 0].bar(['Digitadas', 'Conferidas', 'Cadastradas'], medias_diarias, color=['blue', 'orange', 'green'])
        axs[1, 0].set_title('Média de Transcrições por Dia')
        axs[1, 0].set_ylabel('Quantidade Média')

        axs[1, 1].bar(['Digitadas', 'Conferidas', 'Cadastradas'], medias_funcionarios,
                      color=['blue', 'orange', 'green'])
        axs[1, 1].set_title('Média de Transcrições por Funcionário')
        axs[1, 1].set_ylabel('Quantidade Média')

        plt.tight_layout()

        # Salvar imagem no caminho especificado
        plt.savefig(caminho_imagem)

        plt.show()

    def gerar_pdf(self, texto, caminho_arquivo):
        c = canvas.Canvas(caminho_arquivo, pagesize=letter)
        width, height = letter
        c.drawString(100, height - 40, "Relatório de Progresso")

        y = height - 60
        for linha in texto.split("\n"):
            c.drawString(40, y, linha)
            y -= 20
        c.save()

# Exemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1600x1020")
    app = PageProducaoDetalhes(root, None)
    app.pack(side="top", fill="both", expand=True)
    root.mainloop()
