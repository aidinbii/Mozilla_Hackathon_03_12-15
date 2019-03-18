import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator
from pycorenlp import StanfordCoreNLP
import pandas as pd 


def get_translate(text):
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20190314T122304Z.baa8bdeac71ea044.21fed036c0f8af6c801f0ff61463fc2ff7a09a48&text={0}&lang=en'.format(text)

    page = requests.get(url)

    json_resp = page.json()

    translated_text = json_resp['text'][0]

    return translated_text


def sentiment_stanford(input_text):
    if input_text != '':
        nlp = StanfordCoreNLP('http://localhost:9000')
        res = nlp.annotate(input_text,properties={'annotators': 'sentiment','outputFormat': 'json','timeout': 1000,})
        rows = []
        for s in res["sentences"]:
            rows.append([s["sentimentValue"], s["sentiment"]])
        
        df = pd.DataFrame(rows, columns=['sentiment_value', 'sentiment'])
        df['sentiment_value'] = df['sentiment_value'].apply(float)
        grouped_obj = df.groupby('sentiment')

        scores = {'pos':0.0, 'neu':0.0, 'neg':0.0, 'compound': 0.0}
        for gr_name, gr_df in grouped_obj:
            mean_score = float(gr_df.mean())
            if gr_name == 'Positive':
                scores['pos'] = mean_score
            elif gr_name == 'Negative':
                scores['neg'] = mean_score
            elif gr_name == 'Neutral':
                scores['neu'] = mean_score

        scores['compound'] = scores['pos'] - scores['neg'] + (scores['neu'] / 2.) 
        return scores
    else:
        return None 


def sentiment_analyzer_scores(sentence):
    analyser = SentimentIntensityAnalyzer()
    if sentence != '':
        score = analyser.polarity_scores(sentence)
        return score
    else:
        return None


def google_translate(input_text):
    try:
        translator = Translator()
        a = translator.translate(input_text, dest='en')
        text = a.text
    except:
        text = ''
    return text 


def vader_ensemble(vader_score1, vader_score2):
    if vader_score1 is not None and vader_score2 is not None:
        neg = (vader_score1['neg'] + vader_score2['neg']) / 2.
        pos = (vader_score1['pos'] + vader_score2['pos']) / 2.
        neu = (vader_score1['neu'] + vader_score2['neu']) / 2.
        compound = (vader_score1['compound'] + vader_score2['compound']) / 2.
        return {'neg': neg, 'neu': neu, 'pos': pos, 'compound': compound}
    elif vader_score1 is not None:
        return vader_score1
    elif vader_score2 is not None:
        return vader_score2
    else:
        return 'Something went wrong:('


def stanford_ensemble(stanford_score1, stanford_score2):
    if stanford_score1 is not None and stanford_score2 is not None:
        neg = (stanford_score1['neg'] + stanford_score2['neg']) / 2.
        pos = (stanford_score1['pos'] + stanford_score2['pos']) / 2.
        neu = (stanford_score1['neu'] + stanford_score2['neu']) / 2.
        compound = (stanford_score1['compound'] + stanford_score2['compound']) / 2.
        return {'neg': neg, 'neu': neu, 'pos': pos, 'compound': compound}
    elif stanford_score1 is not None:
        return stanford_score1
    elif stanford_score2 is not None:
        return stanford_score2
    else:
        return 'Something went wrong:('


#input_text = '''Акырында намба приложениясында иштеген нак акчасыз толом пайда болду. Акча салып нак акча боюнча, коопсуздук боюнча убара болбойсун.'''

# input_text = input('... ')

# text = get_translate(input_text)
# text1 = google_translate(input_text)

# vader_yandex_score = sentiment_analyzer_scores(text)
# vader_google_score = sentiment_analyzer_scores(text1)

# vader_scores = vader_ensemble(vader_yandex_score, vader_google_score)

# scores_stanford = sentiment_stanford(text)
# scores_stanford1 = sentiment_stanford(text1)

# stanford_scores = stanford_ensemble(scores_stanford, scores_stanford1)

# print('Dictionary based:', vader_scores)
# print('Deep Learning based:', stanford_scores)

