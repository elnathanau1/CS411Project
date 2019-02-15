from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def dash(request):
   text = "<h1>This is the Dashboard page</h1>"
   return HttpResponse(text)

def connect(request):
  text = '<button type="button">Click Me!</button>'
  return HttpResponse(text)

def group(request):
  text = "<h1>This is the Group page</h1>"
  return HttpResponse(text)

def login(request):
  text = "<h1>This is the Login page</h1>"
  return HttpResponse(text)
