from django.urls import include, path

from users.views import profile
from .views import register, login_view, logout_view, task_list, home
from . import views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('tasks/', task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('', home, name='home'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('complete/<int:task_id>/', views.mark_as_completed, name='mark_as_completed'),
    path('profile/', profile, name='profile'),

    
]