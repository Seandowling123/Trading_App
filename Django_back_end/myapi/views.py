from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from .finance_tools import get_financial_data
import os

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello'})

@api_view(['GET'])
def asdf(request):
    return HttpResponse("<html><body><h1>Hi Clemmy</h1></body></html>", content_type="text/html")

@api_view(['GET'])
def historical_data(request, ticker):
    response = get_financial_data.get_close_with_bands(ticker)
    return Response({'financial_data': response})

@api_view(['GET'])
def index(request):
    # Get the path to the main HTML file of your React app
    react_app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'path_to_react_app', 'index.html')
    # Read the HTML file
    with open(react_app_path, 'r') as file:
        html_content = file.read()
    # Serve the HTML content
    return HttpResponse(html_content)
