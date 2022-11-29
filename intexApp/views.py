from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse

# Create your views here.
loggedIn = False

def indexPageView(request):
    if (loggedIn):
        context = {

        }
        return render(request, 'intexApp/index.html', context)
    else:
        return redirect('login')


def aboutPageView(request):
    if (loggedIn):
        context = {

        }
        return render(request, 'intexApp/about.html')
    else:
        return redirect('login')


def journalPageView(request):
    if (loggedIn):
        context = {

        }
        return render(request, 'intexApp/journal.html')
    else:
        return redirect('login')


def reportPageView(request):
    if (loggedIn): 
        return render(request, 'intexApp/report.html')
    else:
        return redirect('login')


def userPageView(request):
    if (loggedIn): 
        return render(request, 'intexApp/user.html')
    else:
        return redirect('login')


def foodsPageView(request):
    if (loggedIn): 
        return render(request, 'intexApp/myfoods.html')
    else:
        return redirect('login')


def loginPageView(request):
    return render(request, 'intexApp/login.html')
