from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.
def indexPageView(request):
    context = {

    }
    return render(request, 'intexApp/index.html', context)

def aboutPageView(request):
    return render(request, 'intexApp/about.html')

def formPageView(request):
    return render(request, 'intexApp/form.html')