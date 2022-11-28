from django.urls import path
from .views import indexPageView, aboutPageView, formPageView

urlpatterns = [
    path('', indexPageView, name='index'),
    path('about/', aboutPageView, name='about'),
    path('form/', formPageView, name='form'),
    
]
