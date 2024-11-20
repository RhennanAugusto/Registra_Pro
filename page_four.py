import tkinter as tk
from datetime import datetime

class PageFour(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        back_button = tk.Canvas(self, width=40, height=40)
        back_button.create_polygon(10, 20, 30, 10, 30, 30, fill="black")
        back_button.bind("<Button-1>", lambda e: controller.show_frame("StartPage"))
        back_button.pack(anchor="nw", padx=10, pady=10)

        label = tk.Label(self, text="Cartório System", font=("Helvetica", 24))
        label.pack(pady=20)

        label = tk.Label(self, text="3ª CONFERÊNCIA - LIVRO 03 - REGISTRO AUXILIAR", font=("Helvetica", 15))
        label.pack(pady=10)

        center_frame = tk.Frame(self)
        center_frame.pack(expand=True)

        button1 = tk.Button(center_frame, text="Criar meta", font=("Helvetica", 16),
                            command=lambda: controller.show_frame("CadastroDeMetasRegistroAuxiliar"))
        button1.pack(pady=10)

        button2 = tk.Button(center_frame, text="Cadastrar relatorio", font=("Helvetica", 16),
                            command=lambda: controller.show_frame("PageConferenciaLivro03"))
        button2.pack(pady=10)

        button2 = tk.Button(center_frame, text="Historico de Cadastro", font=("Helvetica", 16),
                            command=lambda: controller.show_frame("PageHistoricoRA"))
        button2.pack(pady=10)

        self.add_footer()

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
