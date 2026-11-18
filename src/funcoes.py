from src.config import (
    DICAS_INICIAIS,
    VIDAS_INICIAIS,
    PONTOS_ACERTO,
    BONUS_POR_COMBO,
    BONUS_MAXIMO,
    PENALIDADE_DICA,
    PONTOS_MINIMOS,
    HUMANO,
    IA,
)

def calcular_pontos(pontos_atual, pontos_ganhos):
    """Soma os pontos ganhos à pontuação atual."""
    return pontos_atual + pontos_ganhos


def tomar_dano(vida_atual, dano):
    """Reduz a vida atual com base no dano recebido."""
    return vida_atual - dano


def jogador_perdeu(vidas):
    """Indica se o jogador ficou sem vidas."""
    return vidas <= 0


def limitar_valor(valor, minimo, maximo):
    """Mantém um valor dentro do intervalo [minimo, maximo]."""
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor

def pontos_do_acerto(combo, usou_dica):
    """Pontos de um acerto: base + bônus de combo, menos a penalidade da dica."""
    bonus = limitar_valor(combo * BONUS_POR_COMBO, 0, BONUS_MAXIMO)
    pontos = PONTOS_ACERTO + bonus
    if usou_dica:
        pontos -= PENALIDADE_DICA
    return max(PONTOS_MINIMOS, pontos)


def calcular_tempo_restante(inicio_ms, agora_ms, limite_segundos):
    """Segundos que ainda restam na rodada (nunca menor que zero)."""
    decorrido = (agora_ms - inicio_ms) / 1000
    return max(0.0, limite_segundos - decorrido)


def quebrar_linhas(texto, largura_maxima, medir_largura):
    """Quebra o texto em linhas. `medir_largura(trecho)` devolve a largura em pixels."""
    linhas = []
    atual = ""
    for palavra in texto.split():
        tentativa = (atual + " " + palavra).strip()
        if medir_largura(tentativa) <= largura_maxima:
            atual = tentativa
        else:
            if atual:
                linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas


def nova_partida(textos):
    """Cria o estado inicial de uma partida com a lista de textos sorteados."""
    if not textos:
        raise ValueError("A partida precisa de pelo menos um texto.")
    return {
        "textos": list(textos),
        "indice": 0,
        "vidas": VIDAS_INICIAIS,
        "dicas": DICAS_INICIAIS,
        "pontos": 0,
        "combo": 0,
        "acertos": 0,
        "dica_usada": False,
        "respondida": False,
    }


def texto_atual(partida):
    """Devolve o texto (dicionário) da rodada atual."""
    return partida["textos"][partida["indice"]]


def usar_dica(partida):
    """Gasta uma dica e devolve a pista; devolve None se não for possível."""
    if partida["respondida"] or partida["dica_usada"] or partida["dicas"] <= 0:
        return None
    partida["dicas"] -= 1
    partida["dica_usada"] = True
    return texto_atual(partida)["dica"]


def responder(partida, escolha):
    """Registra a resposta (HUMANO, IA ou None se o tempo esgotou).

    Atualiza pontos, combo e vidas e devolve um dicionário com o resultado.
    """
    if partida["respondida"]:
        raise RuntimeError("Esta rodada já foi respondida.")
    if escolha not in (HUMANO, IA, None):
        raise ValueError("Escolha inválida: " + repr(escolha))

    partida["respondida"] = True
    texto = texto_atual(partida)
    tempo_esgotado = escolha is None
    acertou = (not tempo_esgotado) and escolha == texto["origem"]

    if acertou:
        pontos = pontos_do_acerto(partida["combo"], partida["dica_usada"])
        partida["pontos"] = calcular_pontos(partida["pontos"], pontos)
        partida["combo"] += 1
        partida["acertos"] += 1
    else:
        pontos = 0
        partida["vidas"] = tomar_dano(partida["vidas"], 1)
        partida["combo"] = 0

    return {
        "acertou": acertou,
        "pontos": pontos,
        "origem": texto["origem"],
        "explicacao": texto["explicacao"],
        "tempo_esgotado": tempo_esgotado,
    }


def avancar_rodada(partida):
    """Passa para a próxima rodada (só depois de responder a atual)."""
    if not partida["respondida"]:
        raise RuntimeError("Responda a rodada antes de avançar.")
    partida["indice"] += 1
    partida["dica_usada"] = False
    partida["respondida"] = False


def partida_terminou(partida):
    """A partida acaba ao perder todas as vidas ou ao concluir as rodadas."""
    return jogador_perdeu(partida["vidas"]) or partida["indice"] >= len(partida["textos"])


def partida_venceu(partida):
    """Vitória: concluiu todas as rodadas com pelo menos 1 vida."""
    return partida_terminou(partida) and not jogador_perdeu(partida["vidas"])