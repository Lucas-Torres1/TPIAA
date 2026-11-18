import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    CAMINHO_RECORDE,
    CAMINHO_TEXTOS,
    TOTAL_RODADAS,
    VIDAS_INICIAIS,
    TEMPO_RODADA,
    PENALIDADE_DICA,
    HUMANO,
    IA,
    COR_FUNDO,
    COR_CARTAO,
    COR_TEXTO,
    COR_TEXTO_SUAVE,
    COR_AZUL,
    COR_LARANJA,
    COR_VERDE,
    COR_VERMELHO,
    COR_AMARELO,
    COR_VIDA_PERDIDA,
)
from src.funcoes import (
    nova_partida,
    texto_atual,
    usar_dica,
    responder,
    avancar_rodada,
    partida_terminou,
    partida_venceu,
    calcular_tempo_restante,
    quebrar_linhas,
)
from src.dados import (
    salvar_recorde,
    carregar_recorde,
    carregar_textos,
    sortear_textos,
)

TECLAS_ENTER = (pygame.K_RETURN, pygame.K_KP_ENTER)
MARGEM = 20

# Funções de desenho

def desenhar_texto(tela, conteudo, fonte, cor, x, y, centralizar=False, alinhar_direita=False):
    """Desenha uma linha de texto; (x, y) é o canto, o centro ou a direita."""
    imagem = fonte.render(conteudo, True, cor)
    retangulo = imagem.get_rect()
    if centralizar:
        retangulo.midtop = (x, y)
    elif alinhar_direita:
        retangulo.topright = (x, y)
    else:
        retangulo.topleft = (x, y)
    tela.blit(imagem, retangulo)


def desenhar_paragrafo(tela, conteudo, fonte, cor, x, y, largura, espaco=6):
    """Desenha um texto longo quebrando em várias linhas."""
    for linha in quebrar_linhas(conteudo, largura, lambda t: fonte.size(t)[0]):
        desenhar_texto(tela, linha, fonte, cor, x, y)
        y += fonte.get_height() + espaco


def desenhar_menu(tela, fontes, recorde):
    centro = LARGURA_TELA // 2
    desenhar_texto(tela, TITULO_JOGO, fontes["titulo"], COR_TEXTO, centro, 100, True)
    desenhar_texto(tela, "Este texto foi escrito por um humano ou gerado por IA?",
                   fontes["grande"], COR_TEXTO_SUAVE, centro, 190, True)

    regras = [
        f"{TOTAL_RODADAS} rodadas  |  {TEMPO_RODADA}s por rodada  |  {VIDAS_INICIAIS} vidas",
        "H / seta esquerda: Humano     I / seta direita: IA",
        "D: dica (custa pontos)     Esc: sair",
    ]
    for i, linha in enumerate(regras):
        desenhar_texto(tela, linha, fontes["normal"], COR_TEXTO, centro, 270 + i * 36, True)

    desenhar_texto(tela, f"Recorde: {recorde}", fontes["grande"], COR_AMARELO, centro, 420, True)
    desenhar_texto(tela, "Pressione Enter para começar", fontes["grande"], COR_AZUL, centro, 500, True)


def desenhar_cabecalho(tela, fontes, partida):
    total = len(partida["textos"])
    desenhar_texto(tela, f"Rodada {partida['indice'] + 1}/{total}", fontes["normal"], COR_TEXTO, MARGEM, 20)
    desenhar_texto(tela, f"Pontos: {partida['pontos']}", fontes["normal"], COR_TEXTO, 200, 20)
    desenhar_texto(tela, f"Combo: x{partida['combo']}", fontes["normal"], COR_LARANJA, 340, 20)
    desenhar_texto(tela, f"Dicas: {partida['dicas']}", fontes["normal"], COR_AZUL, 470, 20)
    for i in range(VIDAS_INICIAIS):
        cor = COR_VERMELHO if i < partida["vidas"] else COR_VIDA_PERDIDA
        pygame.draw.circle(tela, cor, (675 + i * 32, 32), 11)


def desenhar_rodada(tela, fontes, partida, fracao_tempo, dica, resultado):
    desenhar_cabecalho(tela, fontes, partida)

    # Barra de tempo
    largura_barra = LARGURA_TELA - 2 * MARGEM
    if fracao_tempo > 0.4:
        cor_barra = COR_VERDE
    elif fracao_tempo > 0.2:
        cor_barra = COR_AMARELO
    else:
        cor_barra = COR_VERMELHO
    pygame.draw.rect(tela, COR_CARTAO, (MARGEM, 62, largura_barra, 12), border_radius=6)
    pygame.draw.rect(tela, cor_barra, (MARGEM, 62, int(largura_barra * fracao_tempo), 12), border_radius=6)

    # Cartão com o texto da rodada
    pygame.draw.rect(tela, COR_CARTAO, (MARGEM, 90, largura_barra, 200), border_radius=14)
    desenhar_paragrafo(tela, texto_atual(partida)["texto"], fontes["grande"], COR_TEXTO,
                       MARGEM + 22, 108, largura_barra - 44)

    if dica:
        desenhar_texto(tela, f"Dica: {dica}", fontes["normal"], COR_AMARELO, MARGEM, 300)

    if resultado is None:
        desenhar_botoes(tela, fontes)
    else:
        desenhar_resultado(tela, fontes, resultado)


def desenhar_botoes(tela, fontes):
    largura = (LARGURA_TELA - 3 * MARGEM) // 2
    botoes = (
        ("[H]  HUMANO", MARGEM, COR_VERDE),
        ("[I]  IA", 2 * MARGEM + largura, COR_AZUL),
    )
    for rotulo, x, cor in botoes:
        pygame.draw.rect(tela, cor, (x, 390, largura, 90), border_radius=14)
        desenhar_texto(tela, rotulo, fontes["grande"], COR_FUNDO, x + largura // 2, 422, True)
    desenhar_texto(tela, f"D: usar dica (-{PENALIDADE_DICA} pontos nesta rodada)",
                   fontes["pequena"], COR_TEXTO_SUAVE, LARGURA_TELA // 2, 505, True)


def desenhar_resultado(tela, fontes, resultado):
    if resultado["tempo_esgotado"]:
        titulo, cor = "Tempo esgotado!", COR_VERMELHO
    elif resultado["acertou"]:
        titulo, cor = f"Acertou! +{resultado['pontos']}", COR_VERDE
    else:
        titulo, cor = "Errou!", COR_VERMELHO

    origem = "escrito por um HUMANO" if resultado["origem"] == HUMANO else "gerado por IA"
    desenhar_texto(tela, titulo, fontes["grande"], cor, MARGEM, 335)
    desenhar_texto(tela, f"Este texto foi {origem}.", fontes["normal"], COR_TEXTO, MARGEM, 375)
    desenhar_paragrafo(tela, resultado["explicacao"], fontes["normal"], COR_TEXTO_SUAVE,
                       MARGEM, 410, LARGURA_TELA - 2 * MARGEM)
    desenhar_texto(tela, "Enter para continuar", fontes["normal"], COR_AZUL,
                   LARGURA_TELA - MARGEM, 560, alinhar_direita=True)


def desenhar_fim(tela, fontes, partida, recorde, novo_recorde):
    centro = LARGURA_TELA // 2
    if partida_venceu(partida):
        titulo, cor = "Vitória!", COR_VERDE
    else:
        titulo, cor = "Fim de jogo", COR_VERMELHO
    desenhar_texto(tela, titulo, fontes["titulo"], cor, centro, 100, True)
    desenhar_texto(tela, f"Pontos: {partida['pontos']}", fontes["grande"], COR_TEXTO, centro, 210, True)
    desenhar_texto(tela, f"Acertos: {partida['acertos']}/{len(partida['textos'])}",
                   fontes["grande"], COR_TEXTO, centro, 260, True)
    if novo_recorde:
        desenhar_texto(tela, "Novo recorde!", fontes["grande"], COR_AMARELO, centro, 320, True)
    else:
        desenhar_texto(tela, f"Recorde: {recorde}", fontes["grande"], COR_AMARELO, centro, 320, True)
    desenhar_texto(tela, "Enter para jogar de novo  |  Esc para sair",
                   fontes["normal"], COR_AZUL, centro, 480, True)


def desenhar_erro(tela, fontes, mensagem):
    desenhar_paragrafo(tela, mensagem, fontes["normal"], COR_VERMELHO, 40, 200, LARGURA_TELA - 80)
    desenhar_texto(tela, "Esc para sair", fontes["normal"], COR_TEXTO_SUAVE, 40, 320)

# Laço principal

def executar_jogo():
    """Executa o loop principal do jogo e controla estado, rodadas e pontuação."""
    pygame.init()

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    relogio = pygame.time.Clock()
    fontes = {
        "titulo": pygame.font.Font(None, 72),
        "grande": pygame.font.Font(None, 34),
        "normal": pygame.font.Font(None, 28),
        "pequena": pygame.font.Font(None, 22),
    }

    recorde = carregar_recorde(CAMINHO_RECORDE)

    # Estados da tela: "menu", "jogando", "resultado", "fim" e "erro"
    estado = "menu"
    partida = None
    resultado = None
    dica = None
    inicio_rodada = 0
    fracao_tempo = 1.0
    novo_recorde = False
    mensagem_erro = ""
    rodando = True

    while rodando:
        relogio.tick(FPS)

        # Entrada
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                continue
            if evento.type != pygame.KEYDOWN:
                continue

            tecla = evento.key
            if tecla == pygame.K_ESCAPE:
                rodando = False

            elif estado in ("menu", "fim") and tecla in TECLAS_ENTER:
                try:
                    textos = carregar_textos(CAMINHO_TEXTOS)
                except (OSError, ValueError, KeyError) as erro:
                    textos = []
                    mensagem_erro = f"Não foi possível ler data/textos.json: {erro}"
                if not textos:
                    if not mensagem_erro:
                        mensagem_erro = "O banco de textos está vazio."
                    estado = "erro"
                else:
                    partida = nova_partida(sortear_textos(textos, TOTAL_RODADAS))
                    novo_recorde = False
                    resultado = None
                    dica = None
                    inicio_rodada = pygame.time.get_ticks()
                    estado = "jogando"

            elif estado == "jogando":
                escolha = None
                if tecla in (pygame.K_h, pygame.K_LEFT):
                    escolha = HUMANO
                elif tecla in (pygame.K_i, pygame.K_RIGHT):
                    escolha = IA
                elif tecla == pygame.K_d:
                    pista = usar_dica(partida)
                    if pista:
                        dica = pista

                if escolha is not None:
                    resultado = responder(partida, escolha)
                    estado = "resultado"

            elif estado == "resultado" and tecla in TECLAS_ENTER:
                avancar_rodada(partida)
                if partida_terminou(partida):
                    if partida["pontos"] > recorde:
                        recorde = partida["pontos"]
                        novo_recorde = True
                        salvar_recorde(CAMINHO_RECORDE, recorde)
                    estado = "fim"
                else:
                    resultado = None
                    dica = None
                    inicio_rodada = pygame.time.get_ticks()
                    estado = "jogando"

        # Atualização 
        if estado == "jogando":
            restante = calcular_tempo_restante(inicio_rodada, pygame.time.get_ticks(), TEMPO_RODADA)
            fracao_tempo = restante / TEMPO_RODADA
            if restante <= 0:
                resultado = responder(partida, None) 
                estado = "resultado"

        # Desenho 
        tela.fill(COR_FUNDO)
        if estado == "menu":
            desenhar_menu(tela, fontes, recorde)
        elif estado in ("jogando", "resultado"):
            desenhar_rodada(tela, fontes, partida, fracao_tempo, dica, resultado)
        elif estado == "fim":
            desenhar_fim(tela, fontes, partida, recorde, novo_recorde)
        elif estado == "erro":
            desenhar_erro(tela, fontes, mensagem_erro)

        pygame.display.flip()

    pygame.quit()