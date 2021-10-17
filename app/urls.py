from django.urls import path


from .views import *

urlpatterns = [
    
    path('',home,name='home'),
    path('download',download,name='download')

]