import tkinter as tk
from datetime import datetime
from page_two import PageTwo
from page_three import PageThree
from page_four import PageFour
from Cadastro_De_Metas_Registro_Geral import CadastroDeMetasRegistroGeral
from page_producao_detalhes import PageProducaoDetalhes
from page_conferencia_livro_02 import PageConferenciaLivro02
from page_conferencia_livro_03 import PageConferenciaLivro03
from Cadastro_de_metas_transcricao import CadastroDeMetasTranscricao
from Cadastro_de_metas_Registro_Auxiliar import CadastroDeMetasRegistroAuxiliar
from page_history import PageHistorico
from page_history_rg import PageHistoricoRG
from page_history_ra import PageHistoricoRA

class CartorioSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cartório System")
        self.geometry("1600x1020")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageTwo, CadastroDeMetasTranscricao, PageThree, CadastroDeMetasRegistroGeral, CadastroDeMetasRegistroAuxiliar, PageFour, PageProducaoDetalhes, PageConferenciaLivro02, PageConferenciaLivro03, PageHistorico, PageHistoricoRG, PageHistoricoRA):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        back_button = tk.Canvas(self, width=40, height=40, highlightthickness=0)
        back_button.create_polygon(10, 20, 30, 10, 30, 30)
        back_button.bind("<Button-1>", lambda e: controller.show_frame("StartPage"))
        back_button.pack(anchor="nw", padx=10, pady=10)

        label = tk.Label(self, text="Cartório System", font=("Helvetica", 24))
        label.pack(pady=20)

        center_frame = tk.Frame(self)
        center_frame.pack(expand=True)

        button1 = tk.Button(center_frame, text="TRANSCRIÇÃO DAS TRANSMISSÕES (LIVRO 03)", font=("Helvetica", 16),
                            command=lambda: controller.show_frame("PageTwo"))
        button1.pack(pady=10)

        button2 = tk.Button(center_frame, text="3ª CONFERÊNCIA - LIVRO 02 - REGISTRO GERAL", font=("Helvetica", 16),
                            command=lambda: controller.show_frame("PageThree"))
        button2.pack(pady=10)

        button3 = tk.Button(center_frame, text="3ª CONFERÊNCIA - LIVRO 03 - REGISTRO AUXILIAR", font=("Helvetica", 16),
                            command=lambda: controller.show_frame("PageFour"))
        button3.pack(pady=10)

        self.add_footer()

    def add_footer(self):
        footer_frame = tk.Frame(self)
        footer_frame.pack(side=tk.BOTTOM, pady=10)

        phrase1 = tk.Label(footer_frame, text="V.1.0.0", font=("Helvetica", 12))
        phrase1.pack(side=tk.LEFT, padx=5)

        separator1 = tk.Label(footer_frame, text="|", font=("Helvetica", 12))
        separator1.pack(side=tk.LEFT, padx=5)

        phrase2 = tk.Label(footer_frame, text="Cartório do 1º Ofício de Notas e Registro de Imóveis", font=("Helvetica", 12))
        phrase2.pack(side=tk.LEFT, padx=5)

        separator2 = tk.Label(footer_frame, text="|", font=("Helvetica", 12))
        separator2.pack(side=tk.LEFT, padx=5)

        current_date = datetime.now().strftime("%d/%m/%Y")
        date_label = tk.Label(footer_frame, text=current_date, font=("Helvetica", 12))
        date_label.pack(side=tk.LEFT, padx=5)

if __name__ == "__main__":
    app = CartorioSystem()
    app.mainloop()
