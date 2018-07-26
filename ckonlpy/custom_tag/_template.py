class SimpleTemplateTagger:
    def __init__(self, templates, dictionary, selector=None):
        self.templates = templates
        self.dictionary = dictionary
        # self.selector = selector if selector else SimpleSelector()

    def _match_words(self, eojeol):
        n = len(eojeol)

        matched = []
        for b in range(n):
            for e in range(b+2, min(n, b + self.dictionary._max_length) + 1):
                word = eojeol[b:e]
                for tag in self.dictionary.get_tags(word):
                    matched.append([word, tag, b, e])
        return matched

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