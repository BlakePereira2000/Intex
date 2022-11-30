from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from .models import User, Food, Food_in_Day, Daily_Journal, Comorbidity

# Create your views here.
loggedIn = True

def authenticate(request):
    user = request.POST.get('user')
    password = request.POST.get('password')
    print
    authUser = User.objects.get(username=user,password=password)
    print(authUser)
    try:
        print(authUser)
        
        return redirect('index')
    except:
        context = {
            'message': 'User not found'
            }
        return render(request,'intexApp/login.html', context)



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

def signupPageView(request):
    return render(request, 'intexApp/signup.html')

