import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class PageHistorico(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Histórico de Registros", font=("Helvetica", 24))
        label.pack(pady=20)

        self.tree = ttk.Treeview(self, columns=("ID", "Data", "Digitadas", "Conferidas", "Cadastradas",
                                                "Meta Id", "Funcionários Digitando",  "Funcionários Conferindo", 
                                                "Funcionários Cadastrando"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Data", text="Data")
        self.tree.heading("Digitadas", text="Digitadas")
        self.tree.heading("Conferidas", text="Conferidas")
        self.tree.heading("Cadastradas", text="Cadastradas")
        self.tree.heading("Meta Id", text= "Meta Id")
        self.tree.heading("Funcionários Digitando", text="Funcionários Digitando")
        self.tree.heading("Funcionários Conferindo", text="Funcionários Conferindo")
        self.tree.heading("Funcionários Cadastrando", text="Funcionários Cadastrando")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.load_data()

        self.tree.bind("<Double-1>", self.on_tree_item_click)

        back_button = tk.Button(self, text="Voltar", command=lambda: controller.show_frame("StartPage"))
        back_button.pack(pady=10)

    def load_data(self):
        conn = sqlite3.connect('transcricoes.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transcricoes_diarias")
        registros = cursor.fetchall()
        for registro in registros:
            self.tree.insert("", tk.END, values=registro)
        conn.close()

    def on_tree_item_click(self, event):
        selected_item = self.tree.selection()[0]
        item_values = self.tree.item(selected_item, "values")
        self.show_edit_form(item_values)

    def show_edit_form(self, item_values):
        edit_window = tk.Toplevel(self)
        edit_window.title("Editar Registro")
        edit_window.geometry("400x400")

        labels = ["Digitadas", "Conferidas", "Cadastradas", "Meta ID", "Funcionários Digitando", "Funcionários Conferindo", "Funcionários Cadastrando"]
        entries = []

        for i, label_text in enumerate(labels):
            label = tk.Label(edit_window, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(edit_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry.insert(0, item_values[i+2])
            entries.append(entry)

        def save_changes():
            try:
                conn = sqlite3.connect('transcricoes.db')
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE transcricoes_diarias SET
                    digitadas = ?, conferidas = ?, cadastradas = ?, meta_id = ?,
                    funcionarios_digitando = ?, funcionarios_conferindo = ?, funcionarios_cadastrando = ?
                    WHERE id = ?
                """, (
                    int(entries[0].get()), int(entries[1].get()), int(entries[2].get()),
                    int(entries[3].get()), int(entries[4].get()), int(entries[5].get()), int(entries[6].get()),
                    item_values[0]
                ))
                conn.commit()
                conn.close()
                messagebox.showinfo("Sucesso", "Registro atualizado com sucesso!")
                edit_window.destroy()
                self.refresh_treeview()
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao atualizar o registro: {e}")

        save_button = tk.Button(edit_window, text="Salvar", command=save_changes)
        save_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

        def delete_record():
                try:
                    conn = sqlite3.connect('transcricoes.db')
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM transcricoes_diarias WHERE id = ?", (item_values[0],))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Sucesso", "Registro excluído com sucesso!")
                    edit_window.destroy()
                    self.refresh_treeview()
                except Exception as e:
                    messagebox.showerror("Erro", f"Ocorreu um erro ao excluir o registro: {e}")

        delete_button = tk.Button(edit_window, text="Excluir", command=delete_record)
        delete_button.grid(row=len(labels), column=1, pady=10)

    def refresh_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.load_data()

