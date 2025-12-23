from django.urls import path
from .views import TaskAnalysisView

urlpatterns = [
    path("analyze/", TaskAnalysisView.as_view(), name="task-analysis"),
]
