from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
import json
from .mvp_hahaha import *

# Create your views here.
def main(request):
    if request.GET.get('search_term'):
        input_text = request.GET.get('search_term')

        text = get_translate(input_text)
        text1 = google_translate(input_text)

        vader_yandex_score = sentiment_analyzer_scores(text)
        vader_google_score = sentiment_analyzer_scores(text1)

        vader_scores = vader_ensemble(vader_yandex_score, vader_google_score)

        scores_stanford = sentiment_stanford(text)
        scores_stanford1 = sentiment_stanford(text1)

        stanford_scores = stanford_ensemble(scores_stanford, scores_stanford1)

        print('Dictionary based:', vader_scores)
        print('Deep Learning based:', stanford_scores)
        data_scores= {}
        data_scores['vader'] = vader_scores
        data_scores['stanford'] = stanford_scores
        print(data_scores)

        return HttpResponse(json.dumps(data_scores, ensure_ascii=False), content_type="application/json")

    context = {}
    data = None
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")




