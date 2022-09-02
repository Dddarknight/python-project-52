from django.contrib import admin
from django.urls import path
from task_manager import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('users/create/',
         views.UserRegistrationFormView.as_view(),
         name='registration'),
    path('users/', views.UsersView.as_view(), name='users'),
    path('login/', views.HexletLoginView.as_view(), name='login'),
    path('logout/', views.HexletLogoutView.as_view(), name='logout'),
    path('users/<int:user_id>/update/',
         views.UpdateView.as_view(),
         name='update'),
    path('users/<int:user_id>/delete/',
         views.DeleteView.as_view(),
         name='delete'),
    path('admin/', admin.site.urls),
]
