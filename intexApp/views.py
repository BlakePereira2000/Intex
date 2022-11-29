from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.
def indexPageView(request):
    context = {

    }
    return render(request, 'intexApp/index.html', context)

def aboutPageView(request):
    return render(request, 'intexApp/about.html')

def journalPageView(request):
    return render(request, 'intexApp/journal.html')

def reportPageView(request):
    return render(request, 'intexApp/report.html')

def userPageView(request):
    return render(request, 'intexApp/user.html')

def foodsPageView(request):
    return render(request, 'intexApp/myfoods.html')

def loginPageView(request):
    return render(request, 'intexApp/login.html')

def signupPageView(request):
    return render(request, 'intexApp/signup.html')