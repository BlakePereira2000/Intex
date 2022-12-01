from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from .models import User, Food, Food_in_Day, Daily_Journal, Comorbidity
import requests
import json
from datetime import date

# Create your views here.

# Create global logged in variable, set it to its default
global loggedIn
loggedIn = False

# create variable for the authenticated in user's id
global auth_user_id
auth_user_id = ''

def authenticate(request):
    user = request.POST.get('user')
    password = request.POST.get('password')
    print(user)
    print(password)
    try:
        auth_user = User.objects.get(username=user,password=password)
        print(auth_user.dob)

        # log the person in
        global loggedIn
        loggedIn = True
        
        # set the global auth_user_id to the user's id
        global auth_user_id
        auth_user_id = auth_user.id

        print(auth_user_id)
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


########### Journal functions ####################
def journalPageView(request):
    global loggedIn
    if (loggedIn):
        
        print(request.GET.get('selected_date'))
        if request.GET.get('selected_date') is None:
            selected_date = date.today()
            print(selected_date)
        else:
            selected_date = request.GET.get('selected_date')

        # Determine the journal we are looking at
        try:
            journal_were_looking_at = Daily_Journal.objects.get(date=selected_date)
            print('already existed')
        except:
            print('need to make new one')
            new_journal = Daily_Journal()
            print(selected_date)
            new_journal.date = selected_date
            global auth_user_id
            new_journal.journal_user = User.objects.get(id=auth_user_id)
            new_journal.save()
            print('journal saved')
            journal_were_looking_at = new_journal

        journalID = journal_were_looking_at.id

        # dateresult = Daily_Journal.objects.get(date=selected_date)

        # if dateresult.count() == 0:
        #     new_journal = Daily_Journal()
        #     new_journal.date = selected_date
        #     new_journal.save()
        #     journal_were_looking_at = new_journal
        # else:
            


        # Get a list of the foods in that day. Find where the journal id of the food in day = the journal id of the journal we are looking at
        foods_in_day = Food_in_Day.objects.filter(journal_id= journalID).select_related('food','journal')

        global auth_user_id
        user_id = auth_user_id
        user = User.objects.get(id=user_id)

        context = {
            'foods_in_day' : foods_in_day,
            'journalID_in_use' : journalID,
            'user' : user,
            'selected_date': selected_date
        }
        return render(request, 'intexApp/journal.html',context)
    else:
        return redirect('login')


# Access "add food to journal" page
def add_food_to_dayPageView(request):
    
    return render(request,'intexApp/add_food_to_day.html')


# Query the existing food db for foods based on search
def food_db_searchView(request):
    # look for term anywhere within title
    term = request.GET['search_string']
    term= term.replace('=', '==').replace('%', '=%').replace('_', '=_')
    term = term.upper()
    resultset = Food.objects.filter(food_name__contains=term)

    context ={
        'resultset': resultset
    }
    return render(request,'intexApp/add_food_to_day.html',context)

# Using the food ID, make a new record of the food in the day
def save_food_to_dayView(request):
    grams = request.POST.get('grams')
    dj_in_use = Daily_Journal.objects.get(id=1) # hardcoded to 1. It should be the journal that is being used.
    dj_in_use.daily_foods.add(request.POST.get('chosenFood'), through_defaults={'grams':grams})
    return redirect('journal')





################### Report Views #####################
def reportPageView(request):
    global loggedIn
    if (loggedIn):

        # sets default to avoid errors
        if request.POST.get('selected_date') is None:
            selectedDate = str(date.today())
        else:
            selectedDate = request.POST.get('selected_date')


        #Get the date selected  from the calendar
        #selectedDate = request.GET['selected_date']

        #Gather all of the records in Daily Journal
        dailyJournals = Daily_Journal.objects.all()
        journalId = 0

        #for every object in dail journals check if the selected date is equal to the
        #date the journal was written, if it is save that journal id
        for dailyJournal in dailyJournals:
            if str(dailyJournal.date) == str(selectedDate):
                journalId = dailyJournal.id

        #gather all of the objects from the food in day table, create an empty food in days list
        foodInDays = Food_in_Day.objects.all()
        foodInDayList = []

        #go through every object in the food in days table, if the journal id for that food in
        #day entry matches the one we have saved then add that food object to the food in days list
        for foodInDay in foodInDays:
            if foodInDay.journal_id == journalId:
                foodInDayList.append(foodInDay)

        #Gather all of the food objects and create an empty food list
        foods = Food.objects.all()
        foodsList = []

        #go through all of the objects in the food in day list, inside of that go through
        #all of the food objects one by one, if the food id of that food is in the food in day
        #list that we have already filtered, then add that food object to the food list
        for foodInDay in foodInDayList:
            for food in foods:
                if food.id == foodInDay.food_id:
                    newFoodObject = {
                        'name': food.food_name,
                        'protein': food.protein,
                        'phosphorus': food.phosphorus,
                        'potassium': food.potassium,
                        'sodium': food.sodium,
                        'water': food.water,
                        'numGrams': foodInDay.grams
                    }
                    foodsList.append(newFoodObject)

        #initializes all of the nutrient count variables
        sodiumCount = 0
        proteinCount = 0
        potassiumCount = 0
        phosphorusCount = 0
        waterCount = 0

        for foodItem in foodsList:
            sodium = foodItem['sodium'] * foodItem['numGrams']
            protein = foodItem['protein'] * foodItem['numGrams']
            phosphorus = foodItem['phosphorus'] * foodItem['numGrams']
            potassium = foodItem['potassium'] * foodItem['numGrams']
            water = foodItem['water'] * foodItem['numGrams']
            sodiumCount += sodium
            proteinCount += protein
            potassiumCount += potassium
            phosphorusCount += phosphorus
            waterCount += water

        context = {
        'sodiumCount': sodiumCount,
        'proteinCount': proteinCount,
        'potassiumCount': potassiumCount,
        'phosphorusCount': phosphorusCount,
        'waterCount': waterCount,
        'selectedDate': selectedDate
        }

        return render(request, 'intexApp/report.html', context)
    else:
        return redirect('login')

def userPageView(request):
    global loggedIn
    if (loggedIn):
        global auth_user_id
        user_id = auth_user_id
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

def updateUserPageView(request):
    if request.method == 'POST':
        global auth_user_id
        id = auth_user_id
        updateUser = User.objects.get(id=id)

        newFirst = request.POST.get('first_name')
        newLast= request.POST.get('last_name')
        newWeight = request.POST.get('weight')
        newHeight = request.POST.get('height')
        newStage = request.POST.get('stage')
    
        updateUser.first_name = newFirst
        updateUser.last_name = newLast
        updateUser.weight = newWeight
        updateUser.height = newHeight
        updateUser.stage = newStage

        updateUser.save()

    global loggedIn
    if (loggedIn):
        user_id = auth_user_id
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
    return render(request, 'intexApp/user.html')  

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
    comorbidityList = Comorbidity.objects.all()
    context = {
        'comorbidityList' : comorbidityList
    }
    return render(request, 'intexApp/signup.html',context)

def savesignupView(request):
    #Check to see if the form method is a get or post
    if request.method == 'POST':
        # Create a new user object from the model
        new_user = User()
        
        same_user = User.objects.filter(username=request.POST.get('username'))
        if same_user.count() > 0:
            print(same_user)
            comorbidityList = Comorbidity.objects.all()
            context = {
            'message': 'Username already in use',
            'comorbidityList' : comorbidityList
            }
            #### if username already in use, basically reload the page in the same way that 
            # 'signup' view does. Redirect to signup
            return render(request, 'intexApp/signup.html',context)


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

            # log them in 
            global loggedIn
            loggedIn = True

            return render(request, 'intexApp/index.html')

def apiSearchPageView(request):
    global loggedIn
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

            # Makes sure foods with duplicate names don't get added.
            duplicateFood = False
            for validItem in validItemList:
                # If the name of the current food is the same as any in the valid list
                if foodItem['description'].replace("'", "") == validItem['name']:
                    duplicateFood = True
            
            # If this food's name is unique
            if duplicateFood == False:
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
                        foodItemObject['protein'] = format(nutrient['value']/100, '.6f')
                    elif nutrient['nutrientName'] in 'Phosphorus, P':
                        nutrientCount += 1
                        foodItemObject['phosphorus'] = format((nutrient['value']/100)/1000, '.6f')
                    elif nutrient['nutrientName'] in 'Potassium, K':
                        nutrientCount += 1
                        foodItemObject['potassium'] = format((nutrient['value']/100)/1000, '.6f')
                    elif nutrient['nutrientName'] in 'Sodium, Na':
                        nutrientCount += 1
                        foodItemObject['sodium'] = format((nutrient['value']/100)/1000, '.6f')
                    elif nutrient['nutrientName'] in 'Water':
                        nutrientCount += 1
                        foodItemObject['water'] = format(nutrient['value']/100, '.6f')
                
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
    global loggedIn
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

