from django.urls import path

from app.api.views import UserListCreateAPIView, ExerciseCreateAPIView, LogListAPIView

urlpatterns = [
    path("users/", UserListCreateAPIView.as_view()),
    path("users/:<_id>/exercises", ExerciseCreateAPIView.as_view()),
    path("users/:<_id>/logs", LogListAPIView.as_view())
]
