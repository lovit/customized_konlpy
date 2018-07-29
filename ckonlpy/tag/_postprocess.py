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
            first_to_ngram[ngram[0]].append(ngram)
        return dict(first_to_ngram)

    def tag(self, phrase):
        def to_replace(w):
            if w in self.replace:
                w_ = self.replace[w]
            elif w[0] in self.replace:
                w_ = self.replace[w[0]]
            else:
                return w
            return (w_, w[1]) if isinstance(w_, str) else w_

        def as_ngram(words):
            # TODO
            return words

        words = self.base_tagger.pos(phrase)

        if self.ngrams:
            words = as_ngram(words)
        if self.stopwords:
            words = [w for w in words if not ((w in self.stopwords) or (w[0] in self.stopwords))]
        if self.passwords:
            words = [w for w in words if ((w in self.passwords) or (w[0] in self.passwords))]
        if self.passtags:
            words = [w for w in words if w[1] in self.passtags]
        if self.replace:
            words = [to_replace(w) for w in words]
        return words