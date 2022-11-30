from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from .models import User, Food, Food_in_Day, Daily_Journal, Comorbidity

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
        return render(request, 'intexApp/user.html')
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


# Render the user signup page with the required dropdowns. (Comorbidities created thru admin)
def signupPageView(request):
    comorbidityList = Comorbidity.objects.all()
    context = {
        'comorbidityList' : comorbidityList
    }
    return render(request, 'intexApp/signup.html',context)


# save the user signup information
def savesignupView(request):
    #Check to see if the form method is a get or post
    if request.method == 'POST':
        # Create a new user object from the model
        new_user = User()
        
        same_user = User.objects.filter(username=request.POST.get('username'))
        if same_user is not None:
            context = {
            'message': 'Username already in use',

            }
            #### if username already in use, basically reload the page in the same way that 
            # 'signup' view does. Redirect to signup
            return redirect(request, 'signup')


        else:
            #Store the data from the form to the new object's attributes (like columns)
            new_user.first_name = request.POST.get('fname')
            new_user.last_name = request.POST.get('lname')
            new_user.username = request.POST.get('username')
            new_user.password = request.POST.get('password')
            new_user.password = request.POST.get('password')
            new_user.dob = request.POST.get('dob')
            new_user.gender = request.POST.get('gender')
            new_user.weight = request.POST.get('weight')
            new_user.height = request.POST.get('height')
            new_user.stage = request.POST.get('stage')
            # Save the new user
            new_user.save()
            print(request.POST.get('comorbidity1'))
            print(request.POST.get('comorbidity2'))
            print(request.POST.get('comorbidity3'))

            # Add the comorbidities. Control for duplicates not required because 'add()' won't allow duplicates
            if request.POST.get('comorbidity1') is not None:
                new_user.comorbidities.add(request.POST.get('comorbidity1'))
            if request.POST.get('comorbidity2') is not None:
                new_user.comorbidities.add(request.POST.get('comorbidity2'))                    
            if request.POST.get('comorbidity3') is not None:
                new_user.comorbidities.add(request.POST.get('comorbidity3'))


            return render(request, 'intexApp/index.html')

