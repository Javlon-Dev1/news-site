from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
    path('auth/login/', LoginView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('auth/register/', RegisterView.as_view()),

]
