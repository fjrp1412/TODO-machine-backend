from django.urls import path, include
from user import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.AuthTokenView.as_view(), name='token')
]
