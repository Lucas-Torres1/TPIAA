# Real ou Gerado?

Projeto final da disciplina de Introdução a Algoritmos/Programação, desenvolvido com Python e Pygame.

## Integrantes do grupo

- Bernardo Duarte
- Gustavo Montanari
- Lucas Torres

## Estrutura do projeto

- `main.py`: ponto de entrada da aplicação.
- `src/`: código-fonte principal do jogo (laço, regras, interface e dados).
- `assets/`: imagens, fontes e sons.
- `data/`: arquivos persistentes (banco de textos e recorde).
- `tests/`: testes unitários com `pytest`.
- `docs/`: documentação do projeto, incluindo a proposta inicial.

## Descrição do jogo

Quiz de decisão rápida sobre conteúdos reais e artificiais. A cada rodada aparece um texto curto, e o jogador precisa decidir se ele foi escrito por um humano ou gerado por IA. Depois de cada resposta, o jogo mostra o resultado e uma pista que explica como reconhecer aquele tipo de texto. O tema de uso responsável aparece na própria mecânica: análise crítica, transparência e cuidado com a confiabilidade do que lemos.

## Objetivo do jogador

Classificar corretamente o maior número possível de textos, terminando a partida com pelo menos 1 vida, e superar o recorde.

## Regras do jogo

- Cada partida tem 12 rodadas, sorteadas de um banco de textos em arquivo.
- O jogador tem 15 segundos por rodada para escolher Humano ou IA.
- Acerto: +10 pontos, com bônus de combo para acertos seguidos.
- Erro ou tempo esgotado: perde 1 vida e o combo zera.
- O jogador tem 3 dicas por partida; usar uma dica revela uma pista, mas reduz os pontos da rodada.
- Vitória: concluir as 12 rodadas com pelo menos 1 vida. Derrota: perder as 3 vidas.
- O recorde é salvo em arquivo na pasta `data/`.

## Controles

- `H` ou seta esquerda: marcar como Humano
- `I` ou seta direita: marcar como IA
- `D`: usar uma dica
- `Enter`: iniciar / avançar
- `Esc`: sair do jogo

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone LINK_DO_REPOSITORIO
cd NOME_DA_PASTA
pip install -r requirements.txt
python main.py
```

## Como executar os testes

```bash
python -m pytest
```

## Recursos externos

Até o momento, nenhum recurso externo é usado além de Python e Pygame. Se forem usados imagens, sons, fontes, código ou tutoriais, serão listados aqui com origem e licença.

Os textos do banco `data/textos.json` foram escritos pelo grupo, já os que foram gerados por ferramenta de IA estão identificados no próprio arquivo.

## Decisões técnicas

- Os textos e o recorde ficam em arquivos JSON.
- A lógica do jogo (pontuação, vidas, combo) fica separada da interface para facilitar os testes.
