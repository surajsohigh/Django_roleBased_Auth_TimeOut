from django.urls import path
from .views import *



# URL patterns
urlpatterns = [
    path('', home, name='home'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
