from django.urls import path
from .views import (
    TodoListApiView,
    TodoDetailViewApi,
)

urlpatterns = [
    path('api', TodoListApiView.as_view()),
    path('api/<int:todo_id>/',TodoDetailViewApi.as_view()),
]