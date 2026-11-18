# Proposta Inicial do Jogo

## 1. Nome provisório do jogo

**Nome:**

> Real ou Gerado?

## 2. Integrantes do grupo

- Nome 1: Bernardo Duarte
- Nome 2: Gustavo Montanari
- Nome 3: Lucas Torres

## 3. Tema escolhido

**Tema:**

> Uso responsável de Inteligência Artificial: reconhecer conteúdo escrito por humanos e conteúdo gerado por IA, com análise crítica e atenção à confiabilidade da informação.

**Como esse tema se relaciona com o jogo?**

> O tema está na própria mecânica: a cada rodada o jogador precisa analisar um texto e decidir se ele é humano ou gerado por IA. Depois da resposta, o jogo explica quais pistas ajudam a reconhecer cada tipo de texto, o que treina o olhar crítico. A dica opcional custa pontos, mostrando que buscar apoio na análise tem um custo, e acertar exige atenção, não sorte.

## 4. Tipo de jogo

**Tipo escolhido:**

> Perguntas e respostas (quiz de decisão rápida), com tempo limite, vidas e combo.

## 5. Descrição geral do jogo

**Descrição:**

> A tela mostra um texto curto, um cronômetro de 15 segundos, a pontuação, as vidas e as dicas restantes. O jogador lê o texto e escolhe se ele foi escrito por um humano ou gerado por IA. Depois de cada resposta, o jogo revela a resposta certa e uma explicação de como reconhecer aquele tipo de texto. O desafio é decidir com pouco tempo, mantendo acertos seguidos para ganhar bônus de combo.

## 6. Objetivo do jogador

**Objetivo:**

> Classificar corretamente o maior número possível de textos, terminando a partida com pelo menos 1 vida e superando o recorde de pontos.

## 7. Regras principais

- Regra 1: Cada partida tem 12 rodadas, sorteadas de um banco de textos em arquivo, e o jogador tem 15 segundos por rodada.
- Regra 2: Acerto vale +10 pontos, com bônus para acertos seguidos (combo).
- Regra 3: Erro ou tempo esgotado tira 1 vida e zera o combo; o jogador começa com 3 vidas.
- Regra 4: O jogador tem 3 dicas por partida; usar uma dica revela uma pista, mas reduz os pontos daquela rodada.
- Regra 5: O recorde de pontos é salvo em arquivo e mostrado no menu e no fim da partida.

## 8. Condição de vitória

**Condição de vitória:**

> Concluir as 12 rodadas com pelo menos 1 vida.

## 9. Condição de derrota ou encerramento

**Condição de derrota ou encerramento:**

> Perder as 3 vidas, por erros ou tempo esgotado, antes de concluir as 12 rodadas.

## 10. Elementos previstos no jogo

- **Personagem ou elemento principal:** O texto da rodada, exibido em um cartão central, e os botões de resposta "Humano" e "IA".
- **Obstáculos ou desafios:** Limite de 15 segundos, textos parecidos entre si e a perda de vidas a cada erro.
- **Itens ou objetos de interação (se houver):** Dicas (3 por partida), que revelam uma pista em troca de pontos.
- **Pontuação, vidas, tempo ou progresso:** Pontuação com combo, 3 vidas, barra de tempo, contador de rodadas (ex.: 5/12) e recorde.

## 11. Controles previstos

**Controles:**

> `H` ou seta esquerda: marcar como Humano. `I` ou seta direita: marcar como IA. `D`: usar uma dica. `Enter`: iniciar e avançar. `Esc`: sair do jogo.

## 12. Principais dificuldades esperadas

- Dificuldade 1: Escrever textos humanos e textos de IA que sejam equilibrados e que não deixem a resposta óbvia.
- Dificuldade 2: Controlar o tempo da rodada e os estados da tela (menu, rodada, resultado, fim) sem bugs.
- Dificuldade 3: Organizar o trabalho em grupo no GitHub e manter a lógica do jogo separada da interface para poder testá-la.

## 13. Escopo mínimo para a entrega final

**Escopo mínimo:**

> Menu inicial, partida de 12 rodadas com texto, cronômetro, botões Humano/IA, pontuação, combo, vidas e dicas, tela de resultado com explicação, tela de fim de jogo (vitória ou derrota) e recorde salvo em arquivo JSON. Um banco com textos suficientes para sortear partidas diferentes.

## 14. Possíveis melhorias, caso haja tempo

- Melhoria 1: Sons de acerto, erro e fim de jogo.
- Melhoria 2: Animações e visual mais elaborado (transições entre rodadas, efeitos no combo).
- Melhoria 3: Mais textos no banco, com categorias ou níveis de dificuldade.
