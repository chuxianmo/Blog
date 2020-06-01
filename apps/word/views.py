from django.shortcuts import render
from django.contrib import messages
from .models import Word
import urllib.request
import json


def search(request):
    """
      @Description: search english word
    """
    if request.method == 'POST':
        word_str = request.POST.get('word')
        try:
            word = Word.objects.get(word__iexact=word_str)
            definition = word.definition
            en_definition = word.en_definition
            uk_audio = word.uk_audio
            us_audio = word.us_audio
            detail = word.detail_url
        except Word.DoesNotExist:
            response = urllib.request.urlopen('https://api.shanbay.com/bdc/search/?word={}'
                                              .format(word_str))
            response = response.read().decode('utf-8')
            data = json.loads(response)
            status_code = data['status_code']
            if status_code == 1:
                messages.add_message(request, messages.ERROR, data['msg'])
                return render(request, 'word/search.html')
            definition = data['data']['definition']
            if data['data']['has_oxford_defn'] and data['data']['has_collins_defn']:
                try:
                    en_definition = data['data']['en_definition']['defn']
                except KeyError:
                    en_definition = ''
            else:
                en_definition = ''
            uk_audio = data['data']['uk_audio']
            us_audio = data['data']['us_audio']
            detail = data['data']['url']
            word = Word.objects.create(word=word_str,
                                       definition=definition,
                                       uk_audio=uk_audio,
                                       us_audio=us_audio,
                                       detail_url=detail,
                                       en_definition=en_definition)
        context = {
            'word': word_str,
            'definition': definition,
            'en_definition': en_definition,
            'uk_audio': uk_audio,
            'us_audio': us_audio,
            'detail': detail
        }
        return render(request, 'word/search.html', context)
    else:
        return render(request, 'word/search.html')
