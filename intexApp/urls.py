from django.urls import path
from .views import indexPageView, aboutPageView, journalPageView, reportPageView, userPageView, foodsPageView

urlpatterns = [
    path('', indexPageView, name='index'),
    path('about/', aboutPageView, name='about'),
    path('journal/', journalPageView, name='journal'),
    path('report/', reportPageView, name='report'),
    path('user/', userPageView, name='user'),
    path('foods/', foodsPageView, name='foods'),
    
]
