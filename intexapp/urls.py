from django.urls import path
from .views import indexPageView, aboutPageView,journalPageView, reportPageView
from .views import userPageView, foodsPageView, loginPageView, signupPageView, savesignupView, authenticate,logoutView, apiSearchPageView, addNewFoodPageView

urlpatterns = [
    path('', indexPageView, name='index'),
    path('about/', aboutPageView, name='about'),
    path('journal/', journalPageView, name='journal'),
    path('report/', reportPageView, name='report'),
    path('user/', userPageView, name='user'),
    path('foods/', foodsPageView, name='foods'),
    path('login/', loginPageView, name='login'),
    path('signup/', signupPageView, name='signup'),
    path('savesignup/', savesignupView, name='savesignup'),
    path('authenticate/', authenticate, name='authenticate'),
    path('logout/', logoutView, name='logout'),
    path('apisearch/', apiSearchPageView, name='apisearch'),
    path('addNewFood/', addNewFoodPageView, name='addNewFood'),

]