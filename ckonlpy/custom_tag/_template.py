class SimpleTemplateTagger:
    def __init__(self, templates, dictionary, selector=None, max_length=10):
        self.templates = templates
        self.dictionary = dictionary
        self.max_length = max_length
        self.selector = selector if selector else SimpleSelector()

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
    
    def set_selector(self, my_weight_dict, my_score_function):
        self.selector.weight = my_weight_dict
        self.selector.score = my_score_function
        test_candidates = [
            [('이', 'Noun'), ('것', 'Noun'), ('은', 'Josa'), ('테', 'Noun'), ('스트', 'Noun')],
            [('이것', 'Noun'), ('은', 'Josa'), ('테', 'Noun'), ('스트', 'Noun')],
            [('이것', 'Noun'), ('은', 'Josa'), ('테스트', 'Noun')]
        ]
        for test_candidate in test_candidates:
            print(test_candidate)
        print('best:', self.selector.select(test_candidates))

class SimpleSelector:
    def __init__(self):
        self.weight = {
            'noun_length': 1,
            'noun_numbers': -0.2,
            'wordlist_length': -0.1,
            'no_noun': -0.5
        }

    def select(self, candidates):
        scores = []
        for candidate in candidates:
            score = self.score(candidate)
            scores.append(score)
        best = sorted(enumerate(scores), key=lambda x:x[1], reverse=True)[0][0]
        return candidates[best]
    
    def score(self, candidate):
        noun_length = sum([len(w) for w, t in candidate if t == 'Noun'])
        noun_numbers = len([1 for w, t in candidate if t == 'Noun'])
        wordlist_length = len(candidate)
        no_noun = 0 if [1 for w, t in candidate if t == 'Noun'] else 1

        return noun_length * self.weight.get('noun_length', 0) + noun_numbers * self.weight.get('noun_numbers', 0) + wordlist_length * self.weight.get('wordlist_length', 0) + no_noun * self.weight.get('no_noun', 0)