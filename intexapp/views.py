from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from .models import User, Food, Food_in_Day, Daily_Journal, Comorbidity
import requests
import json

# Create your views here.
global loggedIn
loggedIn = True

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

        data = Food.objects.all()
        context = {
            "userFoods" : data,
        }
        return render(request, 'intexApp/myfoods.html', context)
    else:
        return redirect('login')


def loginPageView(request):
    return render(request, 'intexApp/login.html')

def signupPageView(request):
    return render(request, 'intexApp/signup.html')

def apiSearchPageView(request):
    if (loggedIn): 

        # Gets search string from user input
        originalSearchString = request.GET['search_string']

        # Cleans string and adds '+' before each word. The '+' ensures that the results contain all words entered.
        # See https://fdc.nal.usda.gov/help.html#bkmk-2 under section 'Using Search Operators' for more information
        searchString = originalSearchString.strip()
        searchString = '+' + searchString.replace(" "," +")

        # Initializes API parameters. dataType refers to the different databases available through the API.
        apiParameters = {
            'api_key': 'TDwP6ToHXnd2lb2a9AroNzd9562GkXW3f63SXuKr',
            'query': searchString,
            'dataType': ['Survey (FNDDS)', 'Foundation', 'SR Legacy']
        }

        # Calls the API and saves the response
        response = requests.get("https://api.nal.usda.gov/fdc/v1/foods/search", params=apiParameters)

        # foodslist contains all the food items found in the search
        rawItemList = response.json()['foods'] 

        # Keeps track of valid results
        ResultCount = 0

        validItemList = []

        # Iterates over food items
        for foodItem in rawItemList:
            
            # This object contains the necessary food information retrieved from the API. 
            # Each food item that has all 5 target nutrients gets added to a list further down.
            foodItemObject = {
                'name': foodItem['description'].replace("'", ""),
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
                    foodItemObject['protein'] = format(nutrient['value']/100, '.4f')
                elif nutrient['nutrientName'] in 'Phosphorus, P':
                    nutrientCount += 1
                    foodItemObject['phosphorus'] = format((nutrient['value']/100), '.4f')
                elif nutrient['nutrientName'] in 'Potassium, K':
                    nutrientCount += 1
                    foodItemObject['potassium'] = format(nutrient['value']/100, '.4f')
                elif nutrient['nutrientName'] in 'Sodium, Na':
                    nutrientCount += 1
                    foodItemObject['sodium'] = format(nutrient['value']/100, '.4f')
                elif nutrient['nutrientName'] in 'Water':
                    nutrientCount += 1
                    foodItemObject['water'] = format(nutrient['value']/100, '.4f')
            
            # If the current food item contains all 5 of the target nutrients, add food object to the list.
            if nutrientCount == 5 :
                ResultCount += 1
                validItemList.append(foodItemObject)
        
        data = Food.objects.all()

        context = {
            'ResultCount': ResultCount,
            'validItemList': validItemList,
            'originalSearchString': originalSearchString,
            'searchString': searchString,
            'userFoods' : data,
        }

        return render(request, 'intexApp/myfoods.html', context)
    else:
        return redirect('login')





def addNewFoodPageView (request):
    if (loggedIn): 
        successfulSave = False
        newFoodName = ''

        if request.method == 'POST':
            chosenFoodItem= request.POST.get('chosenItem')
            chosenFoodItem = json.loads(str(chosenFoodItem).replace("'", "\""))
            
            new_food = Food()

            new_food.food_name = chosenFoodItem['name']
            new_food.protein = chosenFoodItem['protein']
            new_food.phosphorus = chosenFoodItem['phosphorus']
            new_food.potassium = chosenFoodItem['potassium']
            new_food.sodium = chosenFoodItem['sodium']
            new_food.water = chosenFoodItem['water']

            new_food.save()

            successfulSave = True
            newFoodName = chosenFoodItem['name']

        data = Food.objects.all()

        context = {
            'userFoods': data,
            'saved': successfulSave,
            'foodName': newFoodName
        }

        return render(request, 'intexApp/myfoods.html', context)
    else:
        return redirect('login')



''' for adding food to journal from database
# Gets number of grams from user input. If empty, default is 100 g
        numGrams = request.GET['num_grams']
        if numGrams == '':
            numGrams = 100

'''