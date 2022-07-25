from email.mime import base
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user import views

router = DefaultRouter()
app_name = 'user'

router.register(
    '',
    views.UserView,
    basename='user'
)

urlpatterns = [
    path('', include(router.urls))
]
