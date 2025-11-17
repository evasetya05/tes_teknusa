from django.shortcuts import render

def post_media_home(request):
    return render(request, 'media_home.html')
