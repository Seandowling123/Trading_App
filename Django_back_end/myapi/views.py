from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from . import get_financial_data

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello'})

@api_view(['GET'])
def asdf(request):
    return HttpResponse("<html><body><h1>Hello Clemmy</h1></body></html>", content_type="text/html")

@api_view(['GET'])
def historical_data(request, ticker):
    response = get_financial_data.get_close_with_bands(ticker)
    return Response({'financial_data': response})
