import re
from typing import LiteralString


def get_end_pos(start, length, down=True) -> tuple:
    x = start[0] + (length - 1) * down
    y = start[1] + (length - 1) * (not down)
    return (x, y)


def get_word_path(start, down, word) -> tuple:
    end_pos = get_end_pos(start, word_len(word), down)
    if down:
        return ([(i, start[1]) for i in range(
            start[0], end_pos[0] + 1)], end_pos)
    return ([(start[0], i) for i in range(
        start[1], end_pos[1] + 1)], end_pos)


def clear_word(word) -> LiteralString:
    if isinstance(word, list):
        word = ''.join(word)
    return word.replace('[', '').replace(']', '').replace('*', '')


def word_len(word) -> int:
    if isinstance(word, list):
        word = ''.join(word)
    word = clear_word(word)
    return len(word)


def word_split(word) -> list:
    if isinstance(word, list):
        word = ''.join(word)
    word = re.sub(r'\[(\w)\]', r'*\1', word)
    split_result = []
    i = 0
    while i < len(word):
        if word[i] == '*' and i + 1 < len(word):
            split_result.append('*' + word[i + 1])
            i += 2
        else:
            split_result.append(word[i])
            i += 1
    return split_result


def word_join(word) -> str:
    return re.sub(r'\*(\w)', r'[\1]', ''.join(word))
