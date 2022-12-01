from django.urls import path
from .views import indexPageView, aboutPageView,journalPageView, reportPageView, savesignupView
from .views import userPageView, foodsPageView, loginPageView, signupPageView, authenticate,logoutView, apiSearchPageView, addNewFoodPageView
from .views import add_food_to_dayPageView,food_db_searchView, save_food_to_dayView, updateUserPageView, save_journal_editsView

urlpatterns = [
    path('', indexPageView, name='index'),
    path('about/', aboutPageView, name='about'),
    path('journal/', journalPageView, name='journal'),
    path('report/', reportPageView, name='report'),
    path('user/', userPageView, name='user'),
    path('foods/', foodsPageView, name='foods'),
    path('login/', loginPageView, name='login'),
    path('signup/', signupPageView, name='signup'),
    path('authenticate/', authenticate, name='authenticate'),
    path('logout/', logoutView, name='logout'),
    path('apisearch/', apiSearchPageView, name='apisearch'),
    path('addNewFood/', addNewFoodPageView, name='addNewFood'),
    path('savesignup/', savesignupView, name='savesignup'),
    path('add_food_to_day/', add_food_to_dayPageView, name='add_food_to_day'),
    path('food_db_search/', food_db_searchView, name='food_db_search'),
    path('save_food_to_day/', save_food_to_dayView, name='save_food_to_day'),
    path('update_user/', updateUserPageView, name='update_user'),
    path('save_journal_edits/', save_journal_editsView, name='save_journal_edits'), 
]