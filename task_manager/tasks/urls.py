from django.urls import path
from task_manager.tasks import views
from task_manager.tasks.models import Tasks


urlpatterns = [
    path('', views.TasksView.as_view(
         model=Tasks),
         name='tasks'),
    path('create/',
         views.TaskCreationFormView.as_view(),
         name='task_create'),
    path('<int:pk>/update/',
         views.UpdateTaskView.as_view(),
         name='task_update'),
    path('<int:pk>/delete/',
         views.DeleteTaskView.as_view(),
         name='status_delete'),
    path('<int:pk>/',
         views.TaskDescriptionView.as_view(),
         name='task_description'),
]
