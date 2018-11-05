# customized KoNLPy

한국어 자연어처리를 할 수 있는 파이썬 패키지, KoNLPy의 customized version입니다. 

customized_KoNLPy는 확실히 알고 있는 단어들에 대해서는 라이브러리를 거치지 않고 주어진 어절을 아는 단어들로 토크나이징 / 품사판별을 하는 기능을 제공합니다. 이를 위해 template 기반 토크나이징을 수행합니다.

    사전: {'아이오아이': 'Noun', '는': 'Josa'}
    탬플릿: Noun + Josa

위와 같은 단어 리스트와 탬플릿이 있다면 '아이오아이는' 이라는 어절은 [('아이오아이', 'Noun'), ('는', 'Josa')]로 분리됩니다.

## Install

    $ git clone https://github.com/lovit/customized_konlpy.git
    
    $ pip install customized_konlpy

### Requires

- JPype >= 0.6.1
- KoNLPy >= 0.4.4

## Usage

### Part of speech tagging

KoNLPy와 동일하게 Twitter.pos(phrase)를 입력합니다. 각 어절별로 사용자 사전에 알려진 단어가 인식되면 customized_tagger로 어절을 분리하며, 사용자 사전에 알려지지 않은 단어로 구성된 어절은 트위터 형태소 분석기로 처리합니다. 

```python
twitter.pos('우리아이오아이는 이뻐요')
```

    [('우리', 'Noun'), ('아이오', 'Noun'), ('아이', 'Noun'), ('는', 'Josa'), ('이뻐', 'Adjective'), ('요', 'Eomi')] 

'아이오아이'가 알려진 단어가 아니었기 때문에 트위터 분석기에서 단어를 제대로 인식하지 못합니다. 아래의 사용자 사전으로 단어 추가를 한 뒤 동일한 작업을 수행하면 아래와 같은 결과를 얻을 수 있습니다. 

```python
twitter.pos('우리아이오아이는 이뻐요')
``` 

    [('우리', 'Modifier'), ('아이오아이', 'Noun'), ('는', 'Josa'), ('이뻐', 'Adjective'), ('요', 'Eomi')]

```python
twitter.pos('트와이스tt는 좋아요')
```
    [('트와이스', 'Noun'), ('tt', 'Noun'), ('는', 'Josa'), ('좋', 'Adjective'), ('아요', 'Eomi')]

### Add words to dictioanry

ckonlpy.tag의 Twitter는 add_dictionary를 통하여 str 혹은 list of str 형식의 사용자 사전을 추가할 수 있습니다. 

```python
from ckonlpy.tag import Twitter

twitter.add_dictionary('아이오아이', 'Noun')
twitter.add_dictionary(['트와이스', 'tt'], 'Noun')
```

트위터 한국어 분석기에서 이용하지 않는 품사 (단어 클래스)를 추가하고 싶을 경우에는 반드시 force=True로 설정해야 합니다. 

```python
twitter.add_dictionary('lovit', 'Name', force=True)
```

### Add template to customized tagger

현재 사용중인 탬플릿 기반 토크나이저는 코드 사용 중 탬플릿을 추가할 수 있습니다. 현재 사용중인 탬플릿의 리스트는 아래처럼 확인할 수 있습니다. 

```python
twitter.template_tagger.templates
```

    [('Noun', 'Josa'), ('Modifier', 'Noun'), ('Modifier', 'Noun', 'Josa')]

탬플릿은 tuple of str 형식으로 입력합니다. 

```python
twitter.template_tagger.add_a_template(('Noun', 'Noun', 'Josa'))
```

### Set templates tagger selector

Templates를 이용하여도 후보가 여러 개 나올 수 있습니다. 여러 개 후보 중에서 best 를 선택하는 함수를 직접 디자인 할 수 도 있습니다. 이처럼 몇 개의 점수 기준을 만들고, 각 기준의 weight를 부여하는 방식은 트위터 분석기에서 이용하는 방식인데, 직관적이고 튜닝 가능해서 매우 좋은 방식이라 생각합니다.

```python
my_weights = [
    ('num_nouns', -0.1),
    ('num_words', -0.2),
    ('no_noun', -1),
    ('len_sum_of_nouns', 0.2)
]

def my_evaluate_function(candidate):
    num_nouns = len([word for word, pos, begin, e in candidate if pos == 'Noun'])
    num_words = len(candidate)
    has_no_nouns = (num_nouns == 0)
    len_sum_of_nouns = 0 if has_no_nouns else sum(
        (len(word) for word, pos, _, _ in candidate if pos == 'Noun'))

    scores = (num_nouns, num_words, has_no_nouns, len_sum_of_nouns)
    score = sum((score * weight for score, (_, weight) in zip(scores, my_weights)))
    return score
```

위의 예제처럼 my_weights 와 my_evaluate_function 함수를 정의하여 twitter.set_evaluator()에 입력하면, 해당 함수 기준으로 best candidate를 선택합니다.

```python
twitter.set_evaluator(my_weights, my_evaluate_function)
```

### Postprocessor

passwords, stopwords, passtags, 단어 치환을 위한 후처리를 할 수 있습니다. 

passwords 에 등록된 단어, (단어, 품사)만 출력됩니다.

```python
from ckonlpy.tag import Postprocessor

passwords = {'아이오아이', ('정말', 'Noun')}
postprocessor = Postprocessor(twitter, passwords = passwords)
postprocessor.pos('우리아이오아이는 정말 이뻐요')
# [('아이오아이', 'Noun'), ('정말', 'Noun')]
```

stopwords 에 등록된 단어, (단어, 품사)는 출력되지 않습니다. 

```python
stopwords = {'는'}
postprocessor = Postprocessor(twitter, stopwords = stopwords)
postprocessor.pos('우리아이오아이는 정말 이뻐요')
# [('우리', 'Modifier'), ('아이오아이', 'Noun'), ('정말', 'Noun'), ('이뻐', 'Adjective'), ('요', 'Eomi')]
```

특정 품사를 지정하면, 해당 품사만 출력됩니다. 

```python
passtags = {'Noun'}
postprocessor = Postprocessor(twitter, passtags = passtags)
postprocessor.pos('우리아이오아이는 정말 이뻐요')
# [('아이오아이', 'Noun'), ('정말', 'Noun')]
```

치환할 단어, (단어, 품사)를 dict 형식으로 정의하면 tag 에서 단어가 치환되어 출력됩니다.

```python
replace = {'아이오아이': '아이돌', ('이뻐', 'Adjective'): '예쁘다'}
postprocessor = Postprocessor(twitter, replace = replace)
postprocessor.pos('우리아이오아이는 정말 이뻐요')
# [('우리', 'Modifier'), ('아이돌', 'Noun'), ('는', 'Josa'), ('정말', 'Noun'), ('예쁘다', 'Adjective'), ('요', 'Eomi')]
```

연속된 단어를 하나의 단어루 묶기 위해서 nested tuple 이나 tuple of str 형식의 ngram 을 입력할 수 있습니다. tuple of str 의 형식으로 입력된 ngram 은 Noun 으로 인식됩니다.

```python
ngrams = [(('미스', '함무라비'), 'Noun'), ('바람', '의', '나라')]
postprocessor = Postprocessor(twitter, ngrams = ngrams)
postprocessor.pos('미스 함무라비는 재밌는 드라마입니다')
# [('미스 - 함무라비', 'Noun'), ('는', 'Josa'), ('재밌는', 'Adjective'), ('드라마', 'Noun'), ('입니', 'Adjective'), ('다', 'Eomi')]
```

### Loading wordset

utils 에는 stopwords, passwords, replace word pair 를 파일로 저장하였을 경우, 이를 손쉽게 불러오는 함수가 있습니다.

load_wordset 은 set of str 혹은 set of tuple 을 return 합니다. 예시의 passwords.txt 의 내용은 아래와 같습니다. 단어의 품사는 한 칸 띄어쓰기로 구분합니다. stopwords.txt 도 동일한 포멧입니다.

    아이오아이
    아이오아이 Noun
    공연

load_wordset 을 이용하는 예시코드 입니다.

```python
from ckonlpy.utils import load_wordset

passwords = load_wordset('./passwords.txt')
print(passwords) # {('아이오아이', 'Noun'), '아이오아이', '공연'}

stopwords = load_wordset('./stopwords.txt')
print(stopwords) # {'은', '는', ('이', 'Josa')}
```

치환할 단어쌍은 tap 구분이 되어있습니다. 치환될 단어에 품사 태그가 있을 경우 한 칸 띄어쓰기로 구분합니다.

    str\tstr
    str str\tstr

아래는 replacewords.txt 의 예시입니다.

    아빠	아버지
    엄마 Noun	어머니

load_replace_wordpair 을 이용하는 예시코드 입니다.

```python
from ckonlpy.utils import load_replace_wordpair

replace = load_replace_wordpair('./replacewords.txt')
print(replace) # {'아빠': '아버지', ('엄마', 'Noun'): '어머니'}
```

ngram 단어들의 각 단어는 한 칸 띄어쓰기로, ngram 의 품사는 tap 으로 구분되어 있습니다.

    str str
    str str\tstr

아래는 ngrams.txt 의 예시입니다.

    바람 의 나라
    미스 함무라비	Noun

load_ngram 을 이용하는 예시코드 입니다.

```python
from ckonlpy.utils import load_ngram

ngrams = load_ngram('./ngrams.txt')
print(ngrams) # [('바람', '의', '나라'), (('미스', '함무라비'), 'Noun')]
```

## 0.0.6+ vs 0.0.5x

0.0.5x 에서의 변수와 함수의 이름, 변수의 타입 일부를 변경하였습니다.

| 변경 전 | 변경 후 |
| --- | --- |
| ckonlpy.tag.Twitter._loaded_twitter_default_dictionary | ckonlpy.tag.Twitter.use_twitter_dictionary |
| ckonlpy.tag.Twitter._dictionary | ckonlpy.tag.Twitter.dictionary |
| ckonlpy.tag.Twitter._customized_tagger | ckonlpy.tag.Twitter.template_tagger |
| ckonlpy.tag.Postprocessor.tag | ckonlpy.tag.Postprocessor.pos |
| ckonlpy.custom_tag.SimpleSelector | ckonlpy.custom_tag.SimpleEvalator |
| ckonlpy.custom_tag.SimpleSelector.score | ckonlpy.custom_tag.SimpleEvalator.evaluate |
| ckonlpy.tag.Twitter.set_selector | ckonlpy.tag.AbstractTagger.set_evaluator |
| ckonlpy.custom_tag.SimpleSelector.weight | ckonlpy.custom_tag.SimpleEvaluator.weight |

| 변경 후 | 변경 이유 |
| --- | --- |
| ckonlpy.tag.Twitter.use_twitter_dictionary | konlpy.tag.Twitter 의 사전 사용 유무 |
| ckonlpy.tag.Twitter.dictionary | public 으로 변환하였습니다 |
| ckonlpy.tag.Twitter.template_tagger | Template 기반으로 작동하는 tagger 임을 명시하고, public 으로 변환하였습니다 |
| ckonlpy.tag.Postprocessor.pos | 기본 tagger 의 결과를 후처리하는 기능이기 때문에 동일한 함수명으로 통일하였습니다 |
| ckonlpy.custom_tag.SimpleEvalator | 클래스 이름을 Selector 에서 Evaluator 로 변경하였습니다 |
| ckonlpy.custom_tag.SimpleEvalator.evaluate | 품사열 후보의 점수 계산 부분을 score --> evaluate 로 함수명을 변경하였습니다 |
| ckonlpy.tag.AbstractTagger.set_evaluator | 품사열 후보의 점수 계산 함수를 설정하는 함수의 이름을 변경하였습니다. 해당 함수는 ckonlpy.tag.Twitter 에서 ckonlpy.tag.AbstractTagger 로 이동하였습니다 |
| ckonlpy.custom_tag.SimpleEvaluator.weight | {str:float} 형식의 weight 를 [(str, float)] 형식으로 변경하였습니다 |
