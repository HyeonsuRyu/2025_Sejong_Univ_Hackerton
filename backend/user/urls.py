from django.urls import path
from .views import RegisterView, LoginView, PublicProfileView, MyProfileView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/me/', MyProfileView.as_view()),
    path('profile/<str:username>/', PublicProfileView.as_view()),
]