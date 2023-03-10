from django.urls import include, path
from django.views.generic.base import RedirectView
from .views import LoginUserView, RegisterUserView, LogoutUserView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='login_user', permanent=True), name='auth_root'),
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('logout/', LogoutUserView.as_view(), name='logout_user'),
]