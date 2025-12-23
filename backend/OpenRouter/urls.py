from django.urls import path
from .views import (
    AssignmentInitView,
    StepGuideView,
    RecommendModelsView,
    SelectModelView,
    PromptSuggestView,
    ExecuteWithSelectedModelView,
    NextStepView,
)

urlpatterns = [
    path("assignment/", AssignmentInitView.as_view(), name="assignment-init"),
    path("guide/", StepGuideView.as_view(), name="step-guide"),
    path("recommend/", RecommendModelsView.as_view(), name="recommend-models"),
    path("select/", SelectModelView.as_view(), name="select-model"),
    path("prompt/", PromptSuggestView.as_view(), name="prompt-suggest"),
    path("solve/", ExecuteWithSelectedModelView.as_view(), name="execute-selected"),
    path("next/", NextStepView.as_view(), name="next-step"),
]
