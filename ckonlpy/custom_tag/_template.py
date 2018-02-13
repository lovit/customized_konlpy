class SimpleTemplateTagger:
    def __init__(self, templates, dictionary, selector=None, max_length=10):
        self.templates = templates
        self.dictionary = dictionary
        self.max_length = max_length
        self.selector = selector if selector else SimpleSelector()

    def pos(self, eojeol):
        """eojeol: str"""
        
        best_candidates = []
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
                best_candidates += candidates
        
        if best_candidates:
            return self.selector.select(best_candidates)
        
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
            'max_length_of_noun': 0.5,
            'num_of_nouns': -0.2,
            'num_of_words': -0.1,
            'num_noun_is_zero': -0.5
        }

    def select(self, candidates):
        scores = []
        for candidate in candidates:
            score = self.score(candidate)
            scores.append(score)
        best = sorted(enumerate(scores), key=lambda x:x[1], reverse=True)[0][0]
        return candidates[best]
    
    def score(self, candidate):
        num_of_nouns = len([1 for w, t in candidate if t == 'Noun'])
        if num_of_nouns:
            max_length_of_noun = max([len(w) for w, t in candidate if t == 'Noun'])
        else:
            max_length_of_noun = 0
        num_of_words = len(candidate)
        num_noun_is_zero = 0 if num_of_nouns else 1

        return (max_length_of_noun * self.weight.get('max_length_of_noun', 0)
                + num_of_nouns * self.weight.get('noun_numbers', 0)
                + num_of_words * self.weight.get('num_of_words', 0)
                + num_noun_is_zero * self.weight.get('num_noun_is_zero', 0)
               )