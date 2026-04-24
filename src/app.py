import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd


class AutocompleteEntry(tk.Entry):
    def __init__(self, lista, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lista = lista
        self.app = app
        self.var = self["textvariable"] = tk.StringVar()
        self.var.trace("w", self.changed)

        self.listbox = None
        self.frame_lista = None
        self.index = -1

        self.bind("<Down>", self.move_down)
        self.bind("<Up>", self.move_up)
        self.bind("<Return>", self.enter)

    def changed(self, *args):
        texto = self.var.get()

        if texto == "":
            self.fechar_lista()
            return

        palavras = [item for item in self.lista if texto.lower() in item.lower()]

        if palavras:
            if not self.listbox:
                self.frame_lista = tk.Frame(self.master)

                self.scrollbar = tk.Scrollbar(self.frame_lista, orient="vertical")
                self.listbox = tk.Listbox(
                    self.frame_lista,
                    width=self["width"],
                    yscrollcommand=self.scrollbar.set
                )

                self.scrollbar.config(command=self.listbox.yview)

                self.scrollbar.pack(side="right", fill="y")
                self.listbox.pack(side="left", fill="both")

                self.listbox.bind("<<ListboxSelect>>", self.select_item)

            self.frame_lista.place(
                x=self.winfo_x(),
                y=self.winfo_y() + self.winfo_height()
            )

            self.listbox.delete(0, tk.END)

            for p in palavras:
                self.listbox.insert(tk.END, p)

            self.index = -1
        else:
            self.fechar_lista()

    def move_down(self, event):
        if self.listbox:
            if self.index < self.listbox.size() - 1:
                self.index += 1
                self.listbox.select_clear(0, tk.END)
                self.listbox.select_set(self.index)
                self.listbox.activate(self.index)
                self.listbox.see(self.index)
        return "break"

    def move_up(self, event):
        if self.listbox:
            if self.index > 0:
                self.index -= 1
                self.listbox.select_clear(0, tk.END)
                self.listbox.select_set(self.index)
                self.listbox.activate(self.index)
                self.listbox.see(self.index)
        return "break"

    def enter(self, event):
        if self.listbox and self.index >= 0:
            selecionado = self.listbox.get(self.index)
            self.var.set(selecionado)

        self.fechar_lista()
        self.app.adicionar()
        return "break"

    def select_item(self, event):
        if self.listbox:
            selecionado = self.listbox.get(self.listbox.curselection())
            self.var.set(selecionado)
            self.fechar_lista()

    def fechar_lista(self):
        if self.listbox:
            self.frame_lista.destroy()
            self.listbox = None
            self.frame_lista = None
        self.index = -1


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Reagentes")

        self.dados = []
        self.caminho_arquivo = None

        # Título
        titulo = tk.Label(root, text="Inserir Reagentes", font=("Arial", 14, "bold"))
        titulo.pack(pady=(10, 5))

        # Caminho do arquivo
        self.label_arquivo = tk.Label(root, text="Nenhum arquivo carregado", fg="gray")
        self.label_arquivo.pack()

        # Campo
        self.entry = AutocompleteEntry(self.dados, self, root, width=60)
        self.entry.pack(pady=5)

        # Botões
        frame_botoes = tk.Frame(root)
        frame_botoes.pack(pady=10)

        tk.Button(frame_botoes, text="Importar", width=15, command=self.importar).grid(row=0, column=0, padx=5)
        tk.Button(frame_botoes, text="Adicionar", width=15, command=self.adicionar).grid(row=0, column=1, padx=5)
        tk.Button(frame_botoes, text="Excluir", width=15, command=self.excluir).grid(row=0, column=2, padx=5)
        tk.Button(frame_botoes, text="Salvar", width=15, command=self.salvar).grid(row=0, column=3, padx=5)

        # Tabela
        frame_tabela = tk.Frame(root)
        frame_tabela.pack(pady=10, fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_tabela)
        scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            frame_tabela,
            columns=("Reagente",),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        self.tree.heading("Reagente", text="Reagente")
        self.tree.pack(fill="both", expand=True)

        scrollbar.config(command=self.tree.yview)

        # 🔥 Ajuste automático da janela
        self.root.update_idletasks()
        largura = self.root.winfo_reqwidth()
        altura = self.root.winfo_reqheight()
        self.root.geometry(f"{largura}x{altura}")

    def importar(self):
        arquivos = filedialog.askopenfilenames(title="Selecione as tabelas")

        if not arquivos:
            return

        self.caminho_arquivo = arquivos[0]
        self.label_arquivo.config(text=f"Arquivo: {self.caminho_arquivo}", fg="black")

        self.dados.clear()

        for arquivo in arquivos:
            df = pd.read_excel(arquivo) if not arquivo.endswith(".csv") else pd.read_csv(arquivo)
            coluna = df.iloc[:, 1] if df.shape[1] >= 2 else df.iloc[:, 0]
            self.dados.extend(coluna.dropna().astype(str).tolist())

        self.atualizar_tabela()

    def adicionar(self):
        valor = self.entry.get().strip()

        if valor:
            self.dados.append(valor)
            self.tree.insert("", tk.END, values=(valor,))
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "Digite um valor.")

    def excluir(self):
        selecionado = self.tree.selection()

        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um item.")
            return

        for item in selecionado:
            valor = self.tree.item(item, "values")[0]
            if valor in self.dados:
                self.dados.remove(valor)
            self.tree.delete(item)

    def atualizar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for d in self.dados:
            self.tree.insert("", tk.END, values=(d,))

    def salvar(self):
        if not self.caminho_arquivo:
            messagebox.showwarning("Aviso", "Importe um arquivo primeiro.")
            return

        try:
            df = pd.DataFrame(self.dados, columns=["Reagente"])
            df.to_excel(self.caminho_arquivo, index=False)
            messagebox.showinfo("Sucesso", "Arquivo atualizado com sucesso!")
        except PermissionError:
            messagebox.showerror("Erro", "Feche o Excel antes de salvar.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()