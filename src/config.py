# Configurações centrais do jogo (tela, cores, regras e caminhos de arquivos).
import os

LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60

TITULO_JOGO = "Real ou Gerado?"

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (212, 212, 212)

# Cores da interface
COR_FUNDO = (24, 28, 38)
COR_CARTAO = (38, 44, 60)
COR_TEXTO = (235, 238, 245)
COR_TEXTO_SUAVE = (150, 158, 175)
COR_AZUL = (80, 150, 255)
COR_LARANJA = (255, 160, 70)
COR_VERDE = (90, 200, 120)
COR_VERMELHO = (230, 90, 90)
COR_AMARELO = (240, 210, 100)
COR_VIDA_PERDIDA = (70, 70, 80)

# Caminhos
PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_RECORDE = os.path.join(PASTA_PROJETO, "data", "recorde.txt")
CAMINHO_TEXTOS = os.path.join(PASTA_PROJETO, "data", "textos.json")

# Regras da partida
TOTAL_RODADAS = 12
VIDAS_INICIAIS = 3
DICAS_INICIAIS = 3
TEMPO_RODADA = 15  

PONTOS_ACERTO = 10
BONUS_POR_COMBO = 2  
BONUS_MAXIMO = 10
PENALIDADE_DICA = 5
PONTOS_MINIMOS = 1  

HUMANO = "humano"
IA = "ia"