"""
Lab 4
"""

from ngrams.ngram_trie import NGramTrie
import re

def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError

    sentences = re.split('[.!?]', text)
    list_words = []
    for sentence in sentences:
        tokens = re.sub('[^a-z \n]', '', sentence.lower()).split()
        if not tokens:
            continue
        list_words += tokens + ['<END>']

    return tuple(list_words)


class WordStorage:
    def __init__(self):
        self.storage = {}

    def _put_word(self, word: str):
        if not isinstance(word, str) or not word:
            raise ValueError

        if word not in self.storage:
            self.storage[word] = len(self.storage) + 1
        return self.storage[word]

    def get_id(self, word: str) -> int:
        if not isinstance(word, str) or not word:
            raise ValueError

        if word not in self.storage:
            raise KeyError
        return self.storage[word]

    def get_word(self, word_id: int) -> str:
        if not isinstance(word_id, int) or not word_id:
            raise ValueError
        for w, _ in self.storage.items():
            if word_id == _:
                return w
        raise KeyError

    def update(self, corpus: tuple):
        if not isinstance(corpus, tuple):
            raise ValueError
        for word in corpus:
            self._put_word(word)


def encode_text(storage: WordStorage, text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(text, tuple):
        raise ValueError
    return tuple(storage.get_id(word) for word in text)


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or len(context) != self._n_gram_trie.size - 1:
            raise ValueError

        same_begin = []
        for n_gram in self._n_gram_trie.n_grams:
            if context == n_gram[:len(context)]:
                same_begin.append(n_gram)
        if same_begin:
            top_n_grams = sorted(same_begin, key=self._n_gram_trie.n_gram_frequencies.get, reverse=True)
            return top_n_grams[0][-1]
        top_uni_grams = sorted(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get, reverse=True)
        return top_uni_grams[0][0]

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple):
            raise ValueError

        sent = list(context)
        for _ in range(20):
            sent.append(self._generate_next_word(tuple(sent[-(len(context)):])))
            if sent[-1] == self._word_storage.storage['<END>']:
                break
        else:
            sent.append(self._word_storage.storage['<END>'])
        return tuple(sent)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if not isinstance(context, tuple) or not isinstance(number_of_sentences, int):
            raise ValueError

        sent = []
        for _ in range(number_of_sentences):
            new_sent = self._generate_sentence(context)
            if new_sent[len(context) - 1] == self._word_storage.storage['<END>']:
                new_sent = new_sent[len(context):]
            sent.extend(new_sent)
            context = tuple(sent[-len(context):])
        return tuple(sent)



class LikelihoodBasedTextGenerator(NGramTextGenerator):

    def _calculate_maximum_likelihood(self, word: int, context: tuple) -> float:
        pass

    def _generate_next_word(self, context: tuple) -> int:
        pass


class BackOffGenerator(NGramTextGenerator):

    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie, *args):
        super().__init__(word_storage, n_gram_trie)

    def _generate_next_word(self, context: tuple) -> int:
        pass


def decode_text(storage: WordStorage, encoded_text: tuple) -> tuple:
    pass


def save_model(model: NGramTextGenerator, path_to_saved_model: str):
    pass


def load_model(path_to_saved_model: str) -> NGramTextGenerator:
    pass
