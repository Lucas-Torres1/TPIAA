import json

import pytest

from src import dados
from src.config import CAMINHO_TEXTOS, DICAS_INICIAIS, HUMANO, IA, VIDAS_INICIAIS
from src.funcoes import (
    avancar_rodada,
    calcular_pontos,
    calcular_tempo_restante,
    jogador_perdeu,
    limitar_valor,
    nova_partida,
    partida_terminou,
    partida_venceu,
    quebrar_linhas,
    responder,
    tomar_dano,
    usar_dica,
)


def test_calcular_pontos():
    """Deve somar corretamente os pontos atuais com os pontos ganhos."""
    assert calcular_pontos(10, 5) == 15


def test_jogador_perdeu_com_zero_vidas():
    """Deve indicar derrota quando o total de vidas chega a zero."""
    assert jogador_perdeu(0) is True


def test_jogador_nao_perdeu_com_vidas():
    """Nao deve indicar derrota quando o jogador ainda tem vidas."""
    assert jogador_perdeu(3) is False


def test_limitar_valor_abaixo_do_minimo():
    """Deve retornar o limite minimo quando o valor informado for menor."""
    assert limitar_valor(-5, 0, 100) == 0


def test_limitar_valor_acima_do_maximo():
    """Deve retornar o limite maximo quando o valor informado for maior."""
    assert limitar_valor(150, 0, 100) == 100


def test_limitar_valor_dentro_do_intervalo():
    """Deve manter o valor original quando ele ja estiver no intervalo."""
    assert limitar_valor(50, 0, 100) == 50

def fazer_textos(origens):
    return [
        {"texto": f"t{i}", "origem": o, "dica": f"d{i}", "explicacao": f"e{i}"}
        for i, o in enumerate(origens)
    ]

def test_acerto_da_10_pontos_e_sobe_combo():
    p = nova_partida(fazer_textos([HUMANO, IA]))
    r = responder(p, HUMANO)
    assert r["acertou"] and r["pontos"] == 10
    assert p["pontos"] == 10 and p["combo"] == 1 and p["vidas"] == VIDAS_INICIAIS


def test_bonus_de_combo_em_acertos_seguidos():
    p = nova_partida(fazer_textos([HUMANO, IA, HUMANO]))
    responder(p, HUMANO)
    avancar_rodada(p)
    r2 = responder(p, IA)
    avancar_rodada(p)
    r3 = responder(p, HUMANO)
    assert (r2["pontos"], r3["pontos"]) == (12, 14)


def test_erro_perde_vida_e_zera_combo():
    p = nova_partida(fazer_textos([HUMANO, IA]))
    responder(p, HUMANO)
    avancar_rodada(p)
    r = responder(p, HUMANO)  
    assert not r["acertou"] and r["pontos"] == 0
    assert p["vidas"] == VIDAS_INICIAIS - 1 and p["combo"] == 0


def test_tempo_esgotado_conta_como_erro():
    p = nova_partida(fazer_textos([HUMANO]))
    r = responder(p, None)
    assert r["tempo_esgotado"] and not r["acertou"]
    assert p["vidas"] == VIDAS_INICIAIS - 1


def test_dica_reduz_pontos_e_gasta_uma_dica():
    p = nova_partida(fazer_textos([HUMANO]))
    assert usar_dica(p) == "d0"
    assert p["dicas"] == DICAS_INICIAIS - 1
    assert usar_dica(p) is None  
    assert responder(p, HUMANO)["pontos"] == 5


def test_sem_dicas_restantes():
    p = nova_partida(fazer_textos([HUMANO] * 5))
    for _ in range(DICAS_INICIAIS):
        assert usar_dica(p) is not None
        responder(p, HUMANO)
        avancar_rodada(p)
    assert usar_dica(p) is None


def test_derrota_ao_perder_todas_as_vidas():
    p = nova_partida(fazer_textos([HUMANO] * 6))
    for _ in range(VIDAS_INICIAIS):
        responder(p, IA)
        avancar_rodada(p)
    assert partida_terminou(p) and not partida_venceu(p)


def test_vitoria_ao_concluir_todas_as_rodadas_com_vida():
    p = nova_partida(fazer_textos([HUMANO, IA]))
    responder(p, IA)   
    avancar_rodada(p)
    responder(p, IA)   
    avancar_rodada(p)
    assert partida_terminou(p) and partida_venceu(p)


def test_nao_pode_responder_duas_vezes_nem_avancar_sem_responder():
    p = nova_partida(fazer_textos([HUMANO, IA]))
    with pytest.raises(RuntimeError):
        avancar_rodada(p)
    responder(p, HUMANO)
    with pytest.raises(RuntimeError):
        responder(p, HUMANO)


def test_escolha_invalida():
    p = nova_partida(fazer_textos([HUMANO]))
    with pytest.raises(ValueError):
        responder(p, "robo")


def test_partida_sem_textos_da_erro():
    with pytest.raises(ValueError):
        nova_partida([])



def test_tempo_restante():
    assert calcular_tempo_restante(0, 5000, 15) == 10
    assert calcular_tempo_restante(0, 20000, 15) == 0


def test_quebrar_linhas_respeita_largura():
    linhas = quebrar_linhas("aa bb cc dd", 5, len) 
    assert linhas == ["aa bb", "cc dd"]



def test_recorde_salvo_e_lido(tmp_path):
    arquivo = str(tmp_path / "recorde.txt")
    assert dados.carregar_recorde(arquivo) == 0
    dados.salvar_recorde(arquivo, 87)
    assert dados.carregar_recorde(arquivo) == 87


def test_recorde_corrompido_vira_zero(tmp_path):
    arquivo = tmp_path / "recorde.txt"
    arquivo.write_text("abc", encoding="utf-8")
    assert dados.carregar_recorde(str(arquivo)) == 0


def test_banco_de_textos_real_e_valido():
    textos = dados.carregar_textos(CAMINHO_TEXTOS)
    assert len(textos) >= 12
    assert {t["origem"] for t in textos} == {"humano", "ia"}


def test_carregar_textos_ignora_entradas_incompletas(tmp_path):
    arquivo = tmp_path / "t.json"
    arquivo.write_text(json.dumps({"textos": [
        {"texto": "x", "origem": "humano", "dica": "d", "explicacao": "e"},
        {"texto": "sem campos"},
        {"texto": "y", "origem": "alien", "dica": "d", "explicacao": "e"},
    ]}), encoding="utf-8")
    assert len(dados.carregar_textos(str(arquivo))) == 1


def test_sortear_nao_repete_e_respeita_limite():
    textos = fazer_textos([HUMANO] * 5)
    assert len(dados.sortear_textos(textos, 12)) == 5
    sorteio = dados.sortear_textos(textos, 3)
    assert len({t["texto"] for t in sorteio}) == 3