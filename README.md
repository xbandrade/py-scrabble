# 🆂 PyScrabble

🗒️ [README pt-BR](https://github.com/xbandrade/py-scrabble/blob/main/README-pt-BR.md)

## Python implementation of the Scrabble game using words from the Brazilian Portuguese dictionary

### `Scrabble` is a word game where players use letter tiles to create words on a board, scoring points based on the tiles' placement and values.

## 💻 Technologies used:
  - Python 3.12.0
  - Pygame 2.4.0

### ➡️ Local Setup 
- Clone this repository to your machine
- ```python -m venv venv```
- ```pip install -r requirements.txt```
- ```python -m main```

<img src="https://raw.githubusercontent.com/xbandrade/py-scrabble/main/img/game.png">

### ❕PyScrabble Rules and Features
- The words from the dictionary are stored in a `Trie`, and the validity of a word can be efficiently checked through it
- The Scrabble board is implemented as a 15x15 matrix, with many cells having different word and letter multiplier bonuses
- Each Scrabble tile is implemented as a Tile object, with its own letter and value
    - The `blank` tile can represent any letter, but its value will always be zero
- The Scrabble bag of tiles contains all the tiles initially, and each player will get 7 tiles from the bag
- The current player can also choose to exchange tiles from their rack with tiles from the bag
- After playing a word, the player must draw tiles from the bag until they have 7 tiles on their rack
- The goal of the game is to place down the best valid words using the tiles on your rack
- The game ends when one of the players is out of tiles on their rack and the bag of tiles is empty
- If a player spots a possible invalid play by their opponent, they can challenge the previous play
    - If the challenge is accepted, the previous play has to be undone, otherwise the challenger loses their turn
- If no new tiles have been placed down on the board for too many turns, the game ends and the player with the highest score wins

### ❕Player vs Player
- In a Player vs Player game, the players will take turns while their opponent's tiles is hidden
- To play a word, simply click on a board cell to define the direction, then type the word you want to play
    - To play the blank tile, hit the space key before typing the letter and it will be indicated with a different color

### ❕Player vs Bot
- In a Player vs Bot game, the bot will always go for the best possible valid play, which is found by a backtracking algorithm
- If the bot cannot find a valid play, it can either exchange its tiles or challenge the player's previous play
  
