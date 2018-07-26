class SimpleSelector:
    def __init__(self, preference=None):
        self.weight = {
            'max_length_of_noun': 0.5,
            'num_of_nouns': -0.2,
            'num_of_words': -0.1,
            'exist_noun'  : 0.2,
            'single_word' : -0.1
        }
        self.preference = preference if preference else {}

    def select(self, candidates):
        scores = []
        for candidate in candidates:
            score = self.score(candidate)
            scores.append(score)
        best = sorted(enumerate(scores), key=lambda x:x[1], reverse=True)[0][0]
        return candidates[best]

    def score(self, wordpos_list):
        max_length_of_noun = _max_length_of_noun(wordpos_list)
        num_of_nouns = _num_of_nouns(wordpos_list)
        num_of_words = _num_of_words(wordpos_list)
        exist_noun = num_of_nouns > 0
        single_word = num_of_words == 1

        return (max_length_of_noun * self.weight.get('max_length_of_noun', 0)
                + num_of_nouns * self.weight.get('num_of_nouns', 0)
                + num_of_words * self.weight.get('num_of_words', 0)
                + exist_noun * self.weight.get('exist_noun', 0)
                + single_word * self.weight.get('single_word', 0)
               )

def _max_length_of_noun(wordpos_list):
    satisfied = [len(wordpos[0]) for wordpos in wordpos_list if wordpos[1] == 'Noun']
    return max(satisfied) if satisfied else 0

def _num_of_nouns(wordpos_list):
    return len([wordpos for wordpos in wordpos_list if wordpos[1] == 'Noun'])

def _num_of_words(wordpos_list):
    return len(wordpos_list)

def _exist_no_noun(wordpos_list):
    return _num_of_nouns(wordpos_list) == 0