from django.urls import path, include
from .views import GenerateTextView

urlpatterns = [
    path('request/', GenerateTextView.as_view(), name='openrouter-request'),
]