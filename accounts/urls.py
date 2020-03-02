from django.urls import path
from .views import GetUserToken, UserList, UsersDetail

urlpatterns = [
    path('get-user-token/', GetUserToken.as_view()),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UsersDetail.as_view()),
]
