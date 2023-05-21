from django.urls import path
from .views import UserCreateView, login, update_user, delete_user

urlpatterns= [
    path("user_create", UserCreateView.as_view(), name="user_create"),
    path('login/', login),
    path('update_user/<int:user_id>', update_user, name='update_user'),
    path('delete_user/<int:user_id>', delete_user, name='delete_user'),

]