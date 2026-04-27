import tkinter as tk
from tkinter import messagebox
import os
import subprocess

# ===================== CORES (TEMA ESCURO) =====================
BG_COLOR = "#1e1e1e"
FG_COLOR = "#ffffff"
ENTRY_BG = "#2d2d2d"
BTN_BG = "#3c3f41"
BTN_ACTIVE = "#505354"

# ===================== FUNÇÕES =====================

def carregar_caminhos():
    try:
        with open("caminho.txt", encoding="utf-8-sig") as arquivo:
            linhas = arquivo.readlines()

        if len(linhas) < 2:
            messagebox.showerror("Erro", "Arquivo caminho.txt inválido!")
            return

        entrada_origem.delete(0, tk.END)
        entrada_destino.delete(0, tk.END)

        entrada_origem.insert(0, linhas[0].strip())
        entrada_destino.insert(0, linhas[1].strip())

        status_label.config(text="Caminhos carregados com sucesso!", fg="#4caf50")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao ler arquivo:\n{e}")


def salvar():
    try:
        origem = entrada_origem.get().strip()
        destino = entrada_destino.get().strip()

        with open("caminho.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write(origem + "\n")
            arquivo.write(destino + "\n")

        status_label.config(text="Caminhos salvos!", fg="#4caf50")

    except Exception as e:
        messagebox.showerror("Erro", str(e))


def executar_backup():
    origem = entrada_origem.get().strip()
    destino = entrada_destino.get().strip()

    if not origem or not destino:
        messagebox.showwarning("Atenção", "Preencha origem e destino!")
        return

    # validação real do caminho
    if not os.path.exists(origem):
        messagebox.showerror("Erro", "Pasta de origem não existe!")
        status_label.config(text="Erro no backup!", fg="red")
        return

    try:
        comando = ["robocopy", origem, destino, "/MIR"]

        resultado = subprocess.run(comando, capture_output=True, text=True)

        saida = (resultado.stdout + resultado.stderr).lower()

        # detecta erros reais na saída
        erro_real = (
            "error" in saida or
            "falha" in saida or
            "invalid" in saida or
            "não pode" in saida
        )

        # robocopy: 0–7 = OK
        if resultado.returncode <= 7 and not erro_real:
            status_label.config(text="Backup concluído!", fg="#4caf50")
        else:
            status_label.config(text="Erro no backup!", fg="red")
            messagebox.showerror("Erro no backup", resultado.stdout + "\n" + resultado.stderr)

    except Exception as e:
        messagebox.showerror("Erro", str(e))


# ===================== JANELA =====================

janela = tk.Tk()
janela.title("Backup Automatizado")
janela.geometry("520x280")
janela.configure(bg=BG_COLOR)

# ===================== TÍTULO =====================

titulo = tk.Label(
    janela,
    text="Backup Automatizado",
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=("Arial", 14, "bold")
)
titulo.pack(pady=10)

# ===================== ORIGEM =====================

tk.Label(janela, text="Origem:", bg=BG_COLOR, fg=FG_COLOR).pack(anchor="w", padx=60)

entrada_origem = tk.Entry(
    janela,
    width=65,
    bg=ENTRY_BG,
    fg=FG_COLOR,
    insertbackground=FG_COLOR,
    relief="flat",
    justify="left"
)
entrada_origem.pack(pady=5)

# ===================== DESTINO =====================

tk.Label(janela, text="Destino:", bg=BG_COLOR, fg=FG_COLOR).pack(anchor="w", padx=60)

entrada_destino = tk.Entry(
    janela,
    width=65,
    bg=ENTRY_BG,
    fg=FG_COLOR,
    insertbackground=FG_COLOR,
    relief="flat"
)
entrada_destino.pack(pady=5)

# ===================== BOTÕES =====================

frame_botoes = tk.Frame(janela, bg=BG_COLOR)
frame_botoes.pack(pady=15)

btn_carregar = tk.Button(
    frame_botoes,
    text="Carregar caminhos",
    command=carregar_caminhos,
    bg=BTN_BG,
    fg=FG_COLOR,
    activebackground=BTN_ACTIVE,
    relief="flat",
    padx=5,
    pady=5
)
btn_carregar.grid(row=0, column=0, padx=10)

btn_salvar = tk.Button(
    frame_botoes,
    text="Salvar",
    command=salvar,
    bg=BTN_BG,
    fg=FG_COLOR,
    activebackground=BTN_ACTIVE,
    relief="flat",
    padx=10,
    pady=5
)
btn_salvar.grid(row=0, column=1, padx=10)

btn_backup = tk.Button(
    frame_botoes,
    text="Executar Backup",
    command=executar_backup,
    bg=BTN_BG,
    fg=FG_COLOR,
    activebackground=BTN_ACTIVE,
    relief="flat",
    padx=10,
    pady=5
)
btn_backup.grid(row=0, column=2, padx=10)

# ===================== STATUS =====================

status_label = tk.Label(
    janela,
    text="",
    bg=BG_COLOR,
    fg=FG_COLOR
)
status_label.pack(pady=10)

# ===================== LOOP =====================

janela.mainloop()
