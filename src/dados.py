import json
import random

CAMPOS_OBRIGATORIOS = ("texto", "origem", "dica", "explicacao")

def salvar_recorde(caminho_arquivo, pontuacao):
    """Salva a pontuação recorde em arquivo texto."""
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(str(pontuacao))


def carregar_recorde(caminho_arquivo):
    """Carrega o recorde salvo; retorna 0 se não existir valor válido."""
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()

            if conteudo == "":
                return 0

            return int(conteudo)

    except FileNotFoundError:
        return 0

def carregar_textos(caminho_arquivo):
    """Lê o banco de textos (JSON) e ignora entradas incompletas ou inválidas."""
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        conteudo = json.load(arquivo)

    lista = conteudo["textos"] if isinstance(conteudo, dict) else conteudo

    textos_validos = []
    for item in lista:
        completo = all(campo in item for campo in CAMPOS_OBRIGATORIOS)
        if completo and item["origem"] in ("humano", "ia"):
            textos_validos.append(item)
    return textos_validos


def sortear_textos(textos, quantidade):
    """Sorteia até `quantidade` textos, sem repetir."""
    return random.sample(textos, min(quantidade, len(textos)))