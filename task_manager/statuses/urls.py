from django.urls import path
from task_manager.statuses import views


urlpatterns = [
    path('', views.StatusesView.as_view(), name='statuses'),
    path('create/',
         views.StatusCreationFormView.as_view(),
         name='status_create'),
    path('<int:pk>/update/',
         views.UpdateStatusView.as_view(),
         name='status_update'),
    path('<int:pk>/delete/',
         views.DeleteStatusView.as_view(),
         name='status_delete'),
]
