from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from orchestrator import views

urlpatterns = [
    url(r'^', include('orchestrator.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]