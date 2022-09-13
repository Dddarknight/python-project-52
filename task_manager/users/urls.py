from django.urls import path
from task_manager.users import views


urlpatterns = [
    path('create/',
         views.UserRegistrationFormView.as_view(),
         name='registration'),
    path('', views.UsersView.as_view(), name='users'),
    path('<int:pk>/update/',
         views.UpdateView.as_view(),
         name='update'),
    path('<int:pk>/delete/',
         views.DeleteView.as_view(),
         name='delete'),
]
