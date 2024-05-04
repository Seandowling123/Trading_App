from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import get_financial_data

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Peepee Poopoo'})

def historical_data(request, ticker, timeframe):
    response = get_financial_data.get_historical_data(ticker, timeframe)
    return Response({'message': response})
