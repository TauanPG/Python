import tkinter as tk
from tkinter import messagebox, filedialog
import os
import subprocess

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
        # Busca o arquivo no mesmo diretório do script
        caminho_txt = os.path.join(os.path.dirname(__file__), "caminho.txt")
        if not os.path.exists(caminho_txt):
            return  # Apenas ignora se não existir no início

        with open(caminho_txt, "r", encoding="utf-8-sig") as arquivo:
            linhas = [linha.strip() for linha in arquivo.readlines()]

        if len(linhas) >= 2:
            entrada_origem.delete(0, tk.END)
            entrada_destino.delete(0, tk.END)
            entrada_origem.insert(0, linhas[0])
            entrada_destino.insert(0, linhas[1])
            status_label.config(text="Caminhos carregados!", fg=ACCENT_COLOR)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar configurações:\n{e}")


def salvar():
    try:
        origem = entrada_origem.get().strip()
        destino = entrada_destino.get().strip()

        caminho_txt = os.path.join(os.path.dirname(__file__), "caminho.txt")
        with open(caminho_txt, "w", encoding="utf-8") as arquivo:
            arquivo.write(f"{origem}\n{destino}")

        status_label.config(text="Configurações salvas!", fg=ACCENT_COLOR)
    except Exception as e:
        messagebox.showerror("Erro", str(e))


def executar_backup():
    origem = entrada_origem.get().strip()
    destino = entrada_destino.get().strip()

    if not origem or not destino:
        messagebox.showwarning("Atenção", "Preencha origem e destino!")
        return

    if not os.path.exists(origem):
        messagebox.showerror("Erro", "Pasta de origem não encontrada!")
        return

    try:
        status_label.config(text="Backup em andamento...", fg="yellow")
        janela.update_idletasks()  # Atualiza a interface antes de travar no subprocess

        # /R:0 /W:0 evita que o robocopy fique travado tentando copiar arquivos em uso
        comando = ["robocopy", origem, destino, "/MIR", "/R:0", "/W:0"]

        # CREATE_NO_WINDOW = 0x08000000 (Oculta o console no Windows)
        resultado = subprocess.run(comando, capture_output=True, text=True, creationflags=0x08000000)

        # Robocopy codes < 8 são sucessos (8+ indicam falhas críticas)
        if resultado.returncode < 8:
            status_label.config(text="Backup concluído com sucesso!", fg=ACCENT_COLOR)
        else:
            status_label.config(text="Erro crítico no Robocopy!", fg="red")
            messagebox.showerror("Erro", resultado.stdout)

    except Exception as e:
        messagebox.showerror("Erro", f"Falha na execução:\n{e}")


# ===================== JANELA PRINCIPAL =====================
janela = tk.Tk()
janela.title("Backup Robocopy UI")
janela.geometry("550x320")
janela.configure(bg=BG_COLOR)

# Título
tk.Label(janela, text="Backup Automatizado", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 14, "bold")).pack(pady=15)


# Container para campos
def criar_campo(label_text, var_name):
    frame = tk.Frame(janela, bg=BG_COLOR)
    frame.pack(fill="x", padx=40, pady=5)

    tk.Label(frame, text=label_text, bg=BG_COLOR, fg=FG_COLOR).pack(side="left")

    btn_dir = tk.Button(frame, text="📁", command=lambda: selecionar_pasta(var_name),
                        bg=BTN_BG, fg=FG_COLOR, relief="flat", padx=5)
    btn_dir.pack(side="right", padx=5)

    entry = tk.Entry(frame, bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR, relief="flat")
    entry.pack(side="right", fill="x", expand=True)
    return entry


entrada_origem = criar_campo("Origem: ", None)
entrada_destino = criar_campo("Destino: ", None)

# Atribui o comando de seleção após criar os objetos
entrada_origem.master.children['!button'].config(command=lambda: selecionar_pasta(entrada_origem))
entrada_destino.master.children['!button'].config(command=lambda: selecionar_pasta(entrada_destino))

# Botões
frame_botoes = tk.Frame(janela, bg=BG_COLOR)
frame_botoes.pack(pady=20)

botoes_info = [
    ("Carregar", carregar_caminhos),
    ("Salvar", salvar),
    ("Executar Backup", executar_backup)
]

for texto, comando in botoes_info:
    tk.Button(frame_botoes, text=texto, command=comando, bg=BTN_BG, fg=FG_COLOR,
              activebackground=BTN_ACTIVE, relief="flat", padx=15, pady=5).pack(side="left", padx=5)

status_label = tk.Label(janela, text="Pronto", bg=BG_COLOR, fg=FG_COLOR)
status_label.pack()

# Tentar carregar ao iniciar
carregar_caminhos()

janela.mainloop()
