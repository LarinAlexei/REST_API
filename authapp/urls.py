from django.urls import path
from .views import AppUserViewSet

app_name = 'authapp'

urlpatterns = [
    path('', AppUserViewSet.as_view({'get': 'list'})),
]
