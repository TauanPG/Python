import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import os
import subprocess
import threading

# ===================== CORES & ESTILO =====================

BG_COLOR = "#1e1e1e"
FG_COLOR = "#ffffff"
ENTRY_BG = "#2d2d2d"
BTN_BG = "#3c3f41"
BTN_ACTIVE = "#505354"
ACCENT_COLOR = "#4caf50"

# ===================== FUNÇÕES =====================

def selecionar_pasta(entrada):
    caminho = filedialog.askdirectory()

    if caminho:
        entrada.delete(0, tk.END)
        entrada.insert(0, caminho)


def carregar_caminhos():
    try:
        caminho_txt = os.path.join(os.path.dirname(__file__), "caminho.txt")

        if not os.path.exists(caminho_txt):
            return

        with open(caminho_txt, "r", encoding="utf-8-sig") as arquivo:
            linhas = [linha.strip() for linha in arquivo.readlines()]

        if len(linhas) >= 2:
            entrada_origem.delete(0, tk.END)
            entrada_destino.delete(0, tk.END)

            entrada_origem.insert(0, linhas[0])
            entrada_destino.insert(0, linhas[1])

            status_label.config(
                text="Caminhos carregados com sucesso!",
                fg=ACCENT_COLOR
            )

    except Exception as e:
        messagebox.showerror(
            "Erro",
            f"Erro ao carregar configurações:\n{e}"
        )


def salvar():
    try:
        origem = entrada_origem.get().strip()
        destino = entrada_destino.get().strip()

        caminho_txt = os.path.join(os.path.dirname(__file__), "caminho.txt")

        with open(caminho_txt, "w", encoding="utf-8") as arquivo:
            arquivo.write(f"{origem}\n{destino}")

        status_label.config(
            text="Configurações salvas!",
            fg=ACCENT_COLOR
        )

    except Exception as e:
        messagebox.showerror("Erro", str(e))


def executar_backup():
    origem = entrada_origem.get().strip()
    destino = entrada_destino.get().strip()

    if not origem or not destino:
        messagebox.showwarning(
            "Atenção",
            "Preencha origem e destino!"
        )
        return

    if not os.path.exists(origem):
        messagebox.showerror(
            "Erro",
            "Pasta de origem não encontrada!"
        )
        return

    try:
        # Cria destino automaticamente
        os.makedirs(destino, exist_ok=True)

        # Atualiza interface
        status_label.config(
            text="Backup em andamento...",
            fg="yellow"
        )

        progress.start()

        # Comando Robocopy
        comando = [
            "robocopy",
            origem,
            destino,
            "/MIR",
            "/R:0",
            "/W:0"
        ]

        # Arquivo de log
        log_path = os.path.join(
            os.path.dirname(__file__),
            "backup_log.txt"
        )

        with open(log_path, "a", encoding="utf-8") as log:

            resultado = subprocess.run(
                comando,
                stdout=log,
                stderr=log,
                text=True,
                creationflags=0x08000000
            )

        progress.stop()

        # Códigos menores que 8 = sucesso
        if resultado.returncode < 8:

            status_label.config(
                text="Backup concluído com sucesso!",
                fg=ACCENT_COLOR
            )

        else:

            status_label.config(
                text="Erro crítico no backup!",
                fg="red"
            )

            messagebox.showerror(
                "Erro",
                f"Robocopy retornou código: {resultado.returncode}"
            )

    except Exception as e:

        progress.stop()

        messagebox.showerror(
            "Erro",
            f"Falha na execução:\n{e}"
        )


def iniciar_backup_thread():
    thread = threading.Thread(target=executar_backup)

    thread.daemon = True
    thread.start()


def criar_campo(label_text):
    frame = tk.Frame(janela, bg=BG_COLOR)
    frame.pack(fill="x", padx=40, pady=8)

    tk.Label(
        frame,
        text=label_text,
        bg=BG_COLOR,
        fg=FG_COLOR,
        font=("Arial", 10)
    ).pack(side="left")

    entry = tk.Entry(
        frame,
        bg=ENTRY_BG,
        fg=FG_COLOR,
        insertbackground=FG_COLOR,
        relief="flat",
        font=("Arial", 10)
    )

    entry.pack(
        side="right",
        fill="x",
        expand=True,
        padx=(5, 5),
        ipady=5
    )

    btn_dir = tk.Button(
        frame,
        text="📁",
        command=lambda: selecionar_pasta(entry),
        bg=BTN_BG,
        fg=FG_COLOR,
        activebackground=BTN_ACTIVE,
        relief="flat",
        padx=10
    )

    btn_dir.pack(side="right")

    return entry


# ===================== JANELA PRINCIPAL =====================

janela = tk.Tk()

janela.title("Backup Robocopy UI")
janela.geometry("600x350")
janela.configure(bg=BG_COLOR)
janela.resizable(False, False)

# ===================== TÍTULO =====================

tk.Label(
    janela,
    text="Backup Automatizado",
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=("Arial", 16, "bold")
).pack(pady=20)

# ===================== CAMPOS =====================

entrada_origem = criar_campo("Origem:")
entrada_destino = criar_campo("Destino:")

# ===================== BARRA DE PROGRESSO =====================

style = ttk.Style()

style.theme_use("default")

style.configure(
    "green.Horizontal.TProgressbar",
    background=ACCENT_COLOR,
    troughcolor=ENTRY_BG,
    bordercolor=ENTRY_BG,
    lightcolor=ACCENT_COLOR,
    darkcolor=ACCENT_COLOR
)

progress = ttk.Progressbar(
    janela,
    style="green.Horizontal.TProgressbar",
    mode="indeterminate"
)

progress.pack(
    fill="x",
    padx=40,
    pady=20
)

# ===================== BOTÕES =====================

frame_botoes = tk.Frame(janela, bg=BG_COLOR)
frame_botoes.pack(pady=10)

botoes_info = [
    ("Carregar", carregar_caminhos),
    ("Salvar", salvar),
    ("Executar Backup", iniciar_backup_thread)
]

for texto, comando in botoes_info:

    tk.Button(
        frame_botoes,
        text=texto,
        command=comando,
        bg=BTN_BG,
        fg=FG_COLOR,
        activebackground=BTN_ACTIVE,
        relief="flat",
        padx=20,
        pady=8,
        font=("Arial", 10, "bold"),
        cursor="hand2"
    ).pack(side="left", padx=8)

# ===================== STATUS =====================

status_label = tk.Label(
    janela,
    text="Pronto",
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=("Arial", 10)
)

status_label.pack(pady=10)

# ===================== INICIAR =====================

carregar_caminhos()

janela.mainloop()
