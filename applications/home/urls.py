from django.urls import path
from applications.home.views import (
    HomePage
)

app_name = 'home_app'

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
]