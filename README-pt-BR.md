# 🆂 PyScrabble

## Uma implementação do jogo Scrabble em Python usando palavras do dicionário Português Brasileiro

### `Scrabble` é um jogo de palavras onde os jogadores usam peças de letras para criar palavras, marcando pontos baseado no posicionamento e valor das peças.

## 💻 Tecnologias usadas:
  - Python 3.12.0
  - Pygame 2.4.0

### ➡️ Setup Local
- Clone este repositório para sua máquina local
- ```python -m venv venv```
- ```pip install -r requirements.txt```
- ```python -m main```

<img src="https://raw.githubusercontent.com/xbandrade/py-scrabble/main/img/game.png">

### ❕Regras e Features PyScrabble
- As palavras do dicionário são armazenadas em uma `Trie`, e a validade de uma palavra pode ser verificada de forma eficiente por ela
- O tabuleiro de Scrabble foi implementado como uma matriz 15x15, com várias células possuindo diferentes bônus de multiplicador de palavra e letra
- Cada peça de Scrabble foi implementada como um objeto Tile, com sua própria letra e valor
    - A `peça em branco` pode representar qualquer letra, mas seu valor sempre será zero
- A bolsa de peças de Scrabble contém todas as peças inicialmente, e cada jogador deve tirar 7 peças da bolsa
- O jogador atual também pode escolher trocar as peças de seu rack por peças da bolsa
- Depois de jogar uma palavra, o jogador deve retirar peças da bolsa até completar 7 peças em seu rack
- O objetivo do jogo é jogar as melhores palavras válidas utilizando as letras em seu rack
- O jogo termina quando um dos jogadores não possui mais peças e a bolsa de peças estiver vazia
- Se um jogador percebe uma jogada inválida de seu oponente, ele pode desafiar a jogada anterior
    - Se o desafio for aceito, a jogada anterior deve ser desfeita, caso contrário, o desafiante perde sua vez
- Se nenhuma peça nova é jogada por muitos turnos, o jogo termina e o jogador com a maior pontuação vence


### ❕Player vs Player
- Em um jogo de Player vs Player, os jogadores revezam turnos enquanto as peças do oponente estão escondidas
- Para jogar uma palavra, basta clicar na célula do tabuleiro para definir a direção, e então digitar a palavra desejada
    - Para jogar a peça em branco, aperte a tecla de espaço antes de digitar a letra, e ela será indicada com uma cor diferente


### ❕Player vs Bot
- Em um jogo de Player vs Bot, o bot sempre vai fazer a melhor jogada válida possível, que é encontrada por um algoritmo de backtracking
- Se o bot não puder encontrar uma jogada válida, ele pode trocar de peças ou desafiar a jogada anterior do jogador
