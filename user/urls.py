from django.urls import path, include
from user import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.AuthTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('<int:pk>/', views.ManageUserView.as_view(), name='me_detail'),
]
