from django.urls import include, path

from tasks import views
from .views import home, RegisterView, profile, ResetPasswordView

app_name = 'users'

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path("password-reset/", ResetPasswordView.as_view(), name="password-reset"),
]
