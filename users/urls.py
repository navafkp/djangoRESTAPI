from django.urls import path
from .views import RegisterView, LoginView, UserView, UserLogout,UserImageView


urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', UserLogout.as_view()),
    path('upload-image/', UserImageView.as_view()),
]
