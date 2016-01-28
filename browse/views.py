from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("<title>Sweaters But With Peer Reviews</title><h3>Sam Sucks and Dzu Rocks</h3>")
