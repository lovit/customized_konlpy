class SimpleEvaluator:
    def __init__(self, preference=None):
        self.weight = (
            ('max_length_of_noun', 0.5),
            ('length_of_phrase', 0.1),
            ('exist_noun', 0.2),
            ('single_word', -0.1)
        )
        # preference = { (word, pos) : score }
        self.preference = preference if preference else {}
        self.debug = False

    def select(self, candidates):

        def evaluating_format(wordpos_list):
            formed = (
                wordpos_list,
                wordpos_list[0][2],
                wordpos_list[-1][3],
                self.evaluate(wordpos_list)
            )
            return formed

        def is_overlab(b, e, target):
            return (b < target[2]) and (target[1] < e)

        scoreds = [evaluating_format(c) for c in candidates]

        # sorting rules. (score, begin index)
        scoreds = sorted(scoreds, key=lambda x:(-x[3], x[1]))

        selected = []
        while scoreds:
            selected.append(scoreds.pop(0))
            b = selected[-1][1]
            e = selected[-1][2]
            scoreds = [c for c in scoreds if not is_overlab(b, e, c)]

        # sort by begin index
        selected = sorted(selected, key=lambda x:x[1])
        return selected

    def evaluate(self, wordpos_list):

        scores = (
            _max_length_of_noun(wordpos_list),
            wordpos_list[-1][3] - wordpos_list[0][2],
            _num_of_nouns(wordpos_list) > 0,
            _num_of_words(wordpos_list) == 1
        )

        score_sum = _wordpos_preference(wordpos_list, self.preference)

        if self.debug:
            print('\n{}'.format(wordpos_list))
            for score, (field, weight) in zip(scores, self.weight):
                print('{}, w={}, s={}, prod={}'.format(
                        field, weight, score, weight * score))
            print('preference score = {}'.format(score_sum))

        score_sum += sum((score * weight for score, (_, weight)
                          in zip(scores, self.weight)))

        return score_sum

def _max_length_of_noun(wordpos_list):
    satisfied = [len(wordpos[0]) for wordpos in wordpos_list if wordpos[1] == 'Noun']
    return max(satisfied) if satisfied else 0

def _num_of_nouns(wordpos_list):
    return len([wordpos for wordpos in wordpos_list if wordpos[1] == 'Noun'])

def _num_of_words(wordpos_list):
    return len(wordpos_list)

def _wordpos_preference(wordpos_list, preference):
    score = 0
    for word, pos, _, _ in wordpos_list:
        score += preference.get((word, pos), 0)
    return score