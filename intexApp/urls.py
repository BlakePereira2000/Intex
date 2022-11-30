from django.urls import path
from .views import indexPageView, aboutPageView,journalPageView, reportPageView
from .views import userPageView, foodsPageView, loginPageView, signupPageView, authenticate,logoutView

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
]
