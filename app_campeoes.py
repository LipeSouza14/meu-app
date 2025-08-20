import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from PIL import Image, ImageTk
import os

def carregar_json(nome_arquivo):
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar {nome_arquivo}:\n{e}")
        return {}

# Atualiza a aba Campeões
def atualizar_campeao(event=None):
    tipo = combo_tipo.get()
    ano = combo_anos.get()
    if not tipo or not ano:
        return

    dados = dados_campeoes.get(tipo, {})
    campeao = dados.get(ano, "Desconhecido")

    chave = campeao.lower().replace(" ", "_")
    detalhes = {}
    if tipo == "Pilotos":
        detalhes = detalhes_pilotos.get(chave, {})
    else:
        detalhes = detalhes_equipes.get(chave, {})

    texto = f"🏆 Campeão Mundial de {tipo} - {ano}:\n➡️ {campeao}\n\n"
    if detalhes:
        for k, v in detalhes.items():
            texto += f"{k.capitalize()}: {v}\n"
    else:
        texto += "Detalhes não disponíveis.\n"

    text_area_campeoes.delete("1.0", tk.END)
    text_area_campeoes.insert(tk.END, texto)

    nome_imagem = chave + ".png"
    caminho_imagem = os.path.join("imagens", nome_imagem)
    if os.path.exists(caminho_imagem):
        img = Image.open(caminho_imagem)
    else:
        img = Image.new("RGBA", (200, 200), (80, 80, 80, 255))
    img = img.resize((200, 200))
    foto = ImageTk.PhotoImage(img)
    label_imagem_campeoes.config(image=foto)
    label_imagem_campeoes.image = foto

# Atualiza a lista de anos para a aba Campeões
def atualizar_anos(event=None):
    tipo = combo_tipo.get()
    if tipo:
        anos = sorted(dados_campeoes.get(tipo, {}).keys())
        combo_anos["values"] = anos
        if anos:
            combo_anos.set(anos[-1])
            atualizar_campeao()

# Atualiza lista de nomes na aba Estatísticas ao mudar tipo
def carregar_opcoes_estatisticas(event=None):
    tipo = combo_tipo_estatisticas.get()
    if not tipo:
        return

    if tipo == "Pilotos":
        opcoes = sorted(detalhes_pilotos.keys())
    else:
        opcoes = sorted(detalhes_equipes.keys())

    nomes_formatados = [nome.replace("_", " ").title() for nome in opcoes]
    combo_nome_estatisticas["values"] = nomes_formatados
    if nomes_formatados:
        combo_nome_estatisticas.set(nomes_formatados[0])
        mostrar_estatisticas()

# Mostra as estatísticas do piloto ou equipe selecionada
def mostrar_estatisticas(event=None):
    tipo = combo_tipo_estatisticas.get()
    nome_selecionado = combo_nome_estatisticas.get()
    if not tipo or not nome_selecionado:
        return

    chave = nome_selecionado.lower().replace(" ", "_")

    if tipo == "Pilotos":
        dados = detalhes_pilotos.get(chave, {})
    else:
        dados = detalhes_equipes.get(chave, {})

    text_area_estatisticas.delete("1.0", tk.END)

    if not dados:
        text_area_estatisticas.insert(tk.END, "Nenhuma estatística disponível.")
        label_imagem_estatisticas.config(image="", text="Imagem não encontrada", fg="white")
        return

    texto = f"📊 Estatísticas de {nome_selecionado} ({tipo}):\n\n"
    for k, v in dados.items():
        texto += f"{k.capitalize()}: {v}\n"

    text_area_estatisticas.insert(tk.END, texto)

    caminho_img = os.path.join("imagens", chave + ".png")
    if os.path.exists(caminho_img):
        img = Image.open(caminho_img)
    else:
        img = Image.new("RGBA", (200, 200), (80, 80, 80, 255))

    img = img.resize((200, 200))
    foto = ImageTk.PhotoImage(img)
    label_imagem_estatisticas.config(image=foto, text="")
    label_imagem_estatisticas.image = foto

# Carregar dados dos arquivos JSON
dados_campeoes = {
    "Pilotos": carregar_json("campeoes_f1.json"),
    "Construtores": carregar_json("construtores_f1.json")
}
detalhes_pilotos = carregar_json("detalhes_pilotos.json")
detalhes_equipes = carregar_json("detalhes_equipes.json")

# Construção da interface
root = tk.Tk()
root.title("Campeões da Fórmula 1")
root.geometry("540x860")
root.configure(bg="#1e1e1e")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both', padx=10, pady=10)

# Aba Campeões
frame_campeoes = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(frame_campeoes, text="Campeões")

tk.Label(frame_campeoes, text="🏎️ Campeões Mundiais de F1 🏁",
         font=("Arial", 18, "bold"), fg="white", bg="#1e1e1e").pack(pady=15)

frame_tipo = tk.Frame(frame_campeoes, bg="#1e1e1e")
frame_tipo.pack(pady=10)
tk.Label(frame_tipo, text="Tipo:", font=("Arial", 14), fg="white", bg="#1e1e1e").pack(side=tk.LEFT, padx=5)
combo_tipo = ttk.Combobox(frame_tipo, values=["Pilotos", "Construtores"], width=18, font=("Arial", 13))
combo_tipo.pack(side=tk.LEFT)
combo_tipo.bind("<<ComboboxSelected>>", atualizar_anos)

frame_ano = tk.Frame(frame_campeoes, bg="#1e1e1e")
frame_ano.pack(pady=10)
tk.Label(frame_ano, text="Ano:", font=("Arial", 14), fg="white", bg="#1e1e1e").pack(side=tk.LEFT, padx=5)
combo_anos = ttk.Combobox(frame_ano, width=12, font=("Arial", 13))
combo_anos.pack(side=tk.LEFT)
combo_anos.bind("<<ComboboxSelected>>", atualizar_campeao)

text_area_campeoes = scrolledtext.ScrolledText(frame_campeoes, width=60, height=10, bg="#2e2e2e", fg="white",
                                               insertbackground="white", font=("Consolas", 13), relief="sunken", bd=3)
text_area_campeoes.pack(padx=15, pady=15)

label_imagem_campeoes = tk.Label(frame_campeoes, bg="#1e1e1e")
label_imagem_campeoes.pack(pady=10)

# Aba Estatísticas
frame_estatisticas = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(frame_estatisticas, text="Estatísticas")

tk.Label(frame_estatisticas, text="📊 Estatísticas de Pilotos e Equipes",
         font=("Arial", 18, "bold"), fg="white", bg="#1e1e1e").pack(pady=15)

frame_tipo_estat = tk.Frame(frame_estatisticas, bg="#1e1e1e")
frame_tipo_estat.pack(pady=10)
tk.Label(frame_tipo_estat, text="Tipo:", font=("Arial", 14), fg="white", bg="#1e1e1e").pack(side=tk.LEFT, padx=5)
combo_tipo_estatisticas = ttk.Combobox(frame_tipo_estat, values=["Pilotos", "Construtores"], width=18, font=("Arial", 13))
combo_tipo_estatisticas.pack(side=tk.LEFT)
combo_tipo_estatisticas.bind("<<ComboboxSelected>>", carregar_opcoes_estatisticas)

frame_nome_estat = tk.Frame(frame_estatisticas, bg="#1e1e1e")
frame_nome_estat.pack(pady=10)
tk.Label(frame_nome_estat, text="Nome:", font=("Arial", 14), fg="white", bg="#1e1e1e").pack(side=tk.LEFT, padx=5)
combo_nome_estatisticas = ttk.Combobox(frame_nome_estat, width=30, font=("Arial", 13))
combo_nome_estatisticas.pack(side=tk.LEFT)
combo_nome_estatisticas.bind("<<ComboboxSelected>>", mostrar_estatisticas)

text_area_estatisticas = scrolledtext.ScrolledText(frame_estatisticas, width=60, height=10, bg="#2e2e2e", fg="white",
                                                   insertbackground="white", font=("Consolas", 13), relief="sunken", bd=3)
text_area_estatisticas.pack(padx=15, pady=15)

label_imagem_estatisticas = tk.Label(frame_estatisticas, bg="#1e1e1e")
label_imagem_estatisticas.pack(pady=10)

root.mainloop()
