import time
from collections import defaultdict
from typing import Type


class Trie:
    def __init__(self, dict_path: str = None) -> None:
        if not dict_path:
            raise ValueError('Diretório do dicionário deve ser especificado')
        self.dictionary = dict_path
        self.root = TrieNode()
        self.accents_to_remove = {
            'à': 'a', 'á': 'a', 'à': 'a', 'â': 'a',
            'ã': 'a', 'é': 'e', 'ê': 'e', 'í': 'i',
            'ó': 'o', 'ô': 'o', 'õ': 'o', 'ú': 'u',
        }
        self.populate_from_file(dict_path)

    def add_word(self, word: str) -> None:
        word = self.clear_word(word)
        node = self.root
        for letter in word:
            node = node[letter]
        node.is_word = True

    def is_word_valid(self, word: str) -> bool:
        word = self.clear_word(word)
        node = self.root
        for letter in word:
            node = node[letter]
            if not node:
                return False
        return node.is_word

    def populate_from_file(self, filename: str) -> None:
        start_time = time.time()
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                self.add_word(line.strip())
        elapsed_time = time.time() - start_time
        print(f'Trie preenchida em {elapsed_time:.4f} segundos')

    def clear_word(self, word: str) -> str:
        word = word.lower()
        word = word.replace('-', ' ')
        word = word.replace("'", '')
        return ''.join(self.accents_to_remove.get(
            letter, letter) for letter in word)


class TrieNode:
    def __init__(self) -> None:
        self.children = defaultdict(TrieNode)
        self.is_word = False

    def __contains__(self, key: str) -> bool:
        return key in self.children

    def __getitem__(self, key: str) -> Type['TrieNode']:
        return self.children[key]

    def __setitem__(self, key: str, value: Type['TrieNode']) -> None:
        self.children[key] = value
