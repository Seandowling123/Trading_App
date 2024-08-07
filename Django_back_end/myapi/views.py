from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from .finance_tools import get_financial_data, get_trade_history
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello'})

@api_view(['GET'])
def asdf(request):
    return HttpResponse("<html><body><h1>Hi Stephanie</h1></body></html>", content_type="text/html")

@api_view(['GET'])
def historical_data(request, ticker):
    response = get_financial_data.get_close_with_bands(ticker)
    return Response({'financial_data': response})

@api_view(['GET'])
def trade_history(request):
    response = get_trade_history.get_trade_history()
    return Response({'trade_history': response})

@api_view(['GET'])
def account_details(request):
    response = get_trade_history.get_account_summary()
    return Response({'account_details': response})

@api_view(['GET'])
def index(request):
    react_app_path = os.path.join(BASE_DIR, 'build/index.html')
    # Read the HTML file
    with open(react_app_path, 'r') as file:
        html_content = file.read()
    return HttpResponse(html_content, content_type="text/html")
