from django.urls import path
from trajineras.views import *

urlpatterns = [
    path('', index, name='index')

]