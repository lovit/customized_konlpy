from collections import defaultdict

class Postprocessor:
    def __init__(self, base_tagger, stopwords=None,
     passwords=None, passtags=None, replace=None, ngrams=None):
        self.base_tagger = base_tagger
        self.stopwords = stopwords if stopwords else None
        self.passwords = passwords if passwords else None
        self.passtags = passtags if passtags else None
        self.replace = replace if replace else None
        self.ngrams = self._prepare_ngram_converter(ngrams)

    def _prepare_ngram_converter(self, ngrams):
        if not ngrams:
            return None
        first_to_ngram = defaultdict(lambda: [])
        for ngram in ngrams:
            try:
                if isinstance(ngram[0], tuple) and isinstance(ngram[1], str):
                    first_to_ngram[ngram[0][0]].append(ngram)
                elif isinstance(ngram, tuple) and isinstance(ngram[0], str):
                    first_to_ngram[ngram[0]].append((ngram, 'Noun'))
                else:
                    print('ngram format error : {}'.format(ngram))
            except:
                print('ngram format error : {}'.format(ngram))
                continue

        return dict(first_to_ngram)

    def _as_ngram(self, words):
        def same(wordpos_list, ngram_words):
            for wordpos, unigram_word in zip(wordpos_list, ngram_words):
                if (wordpos != unigram_word) and (wordpos[0] != unigram_word):
                    return False
            return True

        words_ = []
        n = len(words)
        idx = 0

        while idx < n:

            candidates = self.ngrams.get(words[idx][0], None)

            if not candidates:
                words_.append(words[idx])
                idx += 1
                continue

            appended = False
            for ngram_words, ngram_pos in candidates:
                stride = len(ngram_words)
                sliced = words[idx:idx+stride]
                if same(sliced, ngram_words):
                    words_.append((' - '.join([w for w, _ in sliced]), ngram_pos))
                    appended = True
                    idx += stride
                    break

            if not appended:
                words_.append(words[idx])
                idx += 1

        return words_

    def pos(self, phrase):
        def to_replace(w):
            if w in self.replace:
                w_ = self.replace[w]
            elif w[0] in self.replace:
                w_ = self.replace[w[0]]
            else:
                return w
            return (w_, w[1]) if isinstance(w_, str) else w_

        words = self.base_tagger.pos(phrase)

        if self.ngrams:
            words = self._as_ngram(words)
        if self.stopwords:
            words = [w for w in words if not ((w in self.stopwords) or (w[0] in self.stopwords))]
        if self.passwords:
            words = [w for w in words if ((w in self.passwords) or (w[0] in self.passwords))]
        if self.passtags:
            words = [w for w in words if w[1] in self.passtags]
        if self.replace:
            words = [to_replace(w) for w in words]
        return words