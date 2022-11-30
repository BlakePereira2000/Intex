from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from .models import User, Food, Food_in_Day, Daily_Journal, Comorbidity
from datetime import date

# Create your views here.
global loggedIn
loggedIn = False

def authenticate(request):
    user = request.POST.get('user')
    password = request.POST.get('password')
    print(user)
    print(password)
    try:
        authUser = User.objects.get(username=user,password=password)
        print(authUser.dob)
        global loggedIn
        loggedIn = True
        return render(request, 'intexApp/index.html')
    except:
        context = {
            'message': 'User not found'
            }
        return render(request,'intexApp/login.html', context)

def logoutView(request):
    global loggedIn 
    loggedIn = False
    return render(request,'intexApp/login.html')



def indexPageView(request):
    global loggedIn
    if (loggedIn):
        context = {

        }
        return render(request, 'intexApp/index.html', context)
    else:
        return redirect('login')


def aboutPageView(request):
    return render(request, 'intexApp/about.html')



def journalPageView(request):
    global loggedIn
    if (loggedIn):
        context = {

        }
        return render(request, 'intexApp/journal.html')
    else:
        return redirect('login')


def reportPageView(request):
    global loggedIn
    if (loggedIn): 
        return render(request, 'intexApp/report.html')
    else:
        return redirect('login')


def userPageView(request):
    global loggedIn
    if (loggedIn):
        user_id = 1
        user = User.objects.get(id=user_id)
        age = date.today().year - (user.dob).year - ((date.today().month, date.today().day) < ((user.dob).month, (user.dob).day))
        gender = user.gender
        context = {
            'user' : user,
            'age' : age,
            'gender' : gender
        }
        return render(request, 'intexApp/user.html', context)

    else:
        return redirect('login')


def foodsPageView(request):
    global loggedIn
    if (loggedIn): 
        return render(request, 'intexApp/myfoods.html')
    else:
        return redirect('login')


def loginPageView(request):
    return render(request, 'intexApp/login.html')

def signupPageView(request):
    return render(request, 'intexApp/signup.html')

