from django.urls import path, include

from rest_framework.routers import DefaultRouter

from workspace import views

router = DefaultRouter()
router.register('', views.WorkspaceViewSet)


app_name = 'workspace'

urlpatterns = [
    path('', include(router.urls))
]
