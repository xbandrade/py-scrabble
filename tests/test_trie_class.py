import pytest

from src import Trie, TrieNode


class TestTrieClass:
    def test_create_new_empty_trie(self):
        trie = Trie()
        assert isinstance(trie.root, TrieNode)
        assert len(trie.root.children) == 0

    def test_insert_word_into_trie(self):
        trie = Trie()
        trie.insert('teste')
        assert len(trie.root.children) == 1
        assert (trie.root.children['t'].children['e'].children['s'].
                children['t'].children['e'].is_word)

    def test_insert_multiple_words_into_trie(self):
        trie = Trie()
        trie.insert('teste')
        trie.insert('adeus')
        assert len(trie.root.children) == 2
        assert (trie.root.children['t'].children['e'].children['s'].
                children['t'].children['e'].is_word)
        assert (trie.root.children['a'].children['d'].children['e'].
                children['u'].children['s'].is_word)

    @pytest.mark.slow
    def test_populate_trie_from_file(self):
        trie = Trie()
        trie.populate_from_file('words_ptbr.txt')
        assert len(trie.root.children)

    def test_search_valid_word_in_trie_returns_true(self):
        trie = Trie()
        trie.insert('teste')
        trie.insert('adeus')
        assert trie.search('teste')

    def test_search_invalid_word_in_trie_returns_false(self):
        trie = Trie()
        trie.insert('teste')
        trie.insert('adeus')
        assert not trie.search('falso')

    def test_clear_word_with_accents(self):
        trie = Trie()
        word = 'ímãs'
        assert trie.clear_word(word) == 'imas'
