from django.shortcuts import render

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

from PyMaker.lt2 import pymaker_service

# Create your views here.
def query(request):
    return render(request, 'Query/query.html')

def answer(request):
    queryText = request.POST['QueryText']
    answerList = pymaker_service.evaluate_query(queryText)

    context = {}
    context['queryText'] = queryText
    context['answerList'] = answerList

    return render(request, 'Query/answer.html', context)