from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from .models import User, Food, Food_in_Day, Daily_Journal, Comorbidity
import requests

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

def signupPageView(request):
    return render(request, 'intexApp/signup.html')

def apiSearchPageView(request):
    if (loggedIn): 

        originalSearchString = request.GET['search_string']
        numGrams = request.GET['num_grams']
        #context = {'yourSearch': searchString}

        # Cleans string and adds '+' before each word. The '+' ensures that the results contain all words entered.
        # See https://fdc.nal.usda.gov/help.html#bkmk-2 under section 'Using Search Operators' for more information
        searchString = originalSearchString.strip()
        searchString = '+' + searchString.replace(" "," +")

        # Initializes API parameters. dataType refers to the databases available through the API.
        apiParameters = {
            'api_key': 'TDwP6ToHXnd2lb2a9AroNzd9562GkXW3f63SXuKr',
            'query': searchString,
            'dataType': ['Survey (FNDDS)', 'Foundation', 'SR Legacy']
        }

        # Calls the API and saves the response
        response = requests.get("https://api.nal.usda.gov/fdc/v1/foods/search", params=apiParameters)

        # foodslist contains all the food items found in the search
        foodsList = response.json()['foods'] 

        # Keeps track of valid results
        FoodCount = 0

        fullItemList = []

        # Iterates over food items
        for foodItem in foodsList:
            
            # This string will contain the name and nutrient information for each valid food item
            foodItemString = foodItem['description'] + '\n'
            foodItemObject = {
                'name': foodItem['description'],
                'protein': '',
                'phosphorus': '',
                'potassium': '',
                'sodium': '',
                'water': '',
            }
            
            #Keeps track of number of target nutrients in each food item
            nutrientCount = 0

            # Iterates over nutrients in a food item
            for nutrient in foodItem['foodNutrients']:

                # If the nutrient is one of the target nutrients
                if nutrient['nutrientName'] in 'Protein':
                    nutrientCount += 1
                    foodItemObject['protein'] = format(nutrient['value']/100*float(numGrams), '.2f')
                    #foodItemString += '     ' + nutrient['nutrientName'] + ': ' + str(nutrient['value']) + ' ' + nutrient['unitName'] + '\n'
                elif nutrient['nutrientName'] in 'Phosphorus, P':
                    nutrientCount += 1
                    foodItemObject['phosphorus'] = format((nutrient['value']/100)*float(numGrams), '.2f')
                elif nutrient['nutrientName'] in 'Potassium, K':
                    nutrientCount += 1
                    foodItemObject['potassium'] = format(nutrient['value']/100*float(numGrams), '.2f')
                elif nutrient['nutrientName'] in 'Sodium, Na':
                    nutrientCount += 1
                    foodItemObject['sodium'] = format(nutrient['value']/100*float(numGrams), '.2f')
                elif nutrient['nutrientName'] in 'Water':
                    nutrientCount += 1
                    foodItemObject['water'] = format(nutrient['value']/100*float(numGrams), '.2f')
            
            # If the food item contains all 5 of the target nutrients
            if nutrientCount == 5 :
                FoodCount += 1
                fullItemList.append(foodItemObject)
        

        context = {
            'num_grams': numGrams,
            'FoodCount': FoodCount,
            'fullItemList': fullItemList,
            'originalSearchString': originalSearchString,
            'searchString': searchString,
        }



        return render(request, 'intexApp/myfoods.html', context)
    else:
        return redirect('login')
