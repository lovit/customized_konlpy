class Postprocessor:
    def __init__(self, base_tagger, stopwords=None, passwords=None, only_tags=None, replace=None):
        self.base_tagger = base_tagger
        self.stopwords = stopwords if stopwords else None
        self.passwords = passwords if passwords else None
        self.only_tags = only_tags if only_tags else None
        self.replace = replace if replace else None
        
    def tag(self, phrase):
        def to_replace(w):
            if w in self.replace: return self.replace[w]
            if w[0] in self.replace: return (self.replace[w[0]], w[1])
            return w

        words = self.base_tagger.pos(phrase)
        if self.stopwords:
            words = [w for w in words if not ((w in self.stopwords) or (w[0] in self.stopwords))]
        if self.passwords:
            words = [w for w in words if ((w in self.passwords) or (w[0] in self.passwords))]
        if self.only_tags:
            words = [w for w in words if w[1] in self.only_tags]
        if self.replace:
            words = [to_replace(w) for w in words]
        return words