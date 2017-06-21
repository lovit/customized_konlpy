class SimpleTemplateTagger:
    def __init__(self, templates, dictionary, selector, max_length=10):
        self.templates = templates
        self.dictionary = dictionary
        self.max_length = max_length
        self.selector = selector

    def pos(self, eojeol):
        """eojeol: str"""

        for template in self.templates:
            n = len(eojeol)
            
            # Initialize
            candidates = []
            for e in range(1, min(self.max_length, n)+1):
                word = eojeol[:e]
                if self.dictionary.is_tag(word, template[0]):
                    candidates.append([(word, template[0], e)])
            if not candidates:
                continue

            # Expansion
            for t in template[1:]:
                candidates_ = []
                for candidate in candidates:
                    word, t0, b = candidate[-1]
                    for e in range(b, min(self.max_length+b, n)+1):
                        word = eojeol[b:e]
                        if self.dictionary.is_tag(word, t):
                            candidates_.append(candidate + [(word, t, e)])
                candidates = candidates_
                if not candidates:
                    break

            # Select best one
            candidates = [[tagged[:2] for tagged in c] for c in candidates if c[-1][2] == n]
            if candidates:
                return self.selector.select(candidates)

        return None
    
    def add_a_template(self, a_template):
        if type(a_template) != tuple:
            a_template = tuple(a_template)
        if (a_template in self.templates) == False:
            self.templates.append(a_template)