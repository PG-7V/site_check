from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def keywords_view(request):
    return render(request, 'src/keywords.html')
