from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ModelViewSet
from authapp.models import ApiUser
from authapp.serializers import AppUsersSerializer
from rest_framework import permissions


class AppUserViewSet(ModelViewSet):
    renderer_classes = [JSONRenderer]
    queryset = ApiUser.objects.all()
    serializer_class = AppUsersSerializer
    permission_classes = [permissions.IsAuthenticated]


# class AppUserViewSet(ListAPIView,
#                     RetrieveAPIView,
#                     GenericAPIView):
#    renderer_classes = [JSONRenderer]
#    queryset = ApiUser.objects.all()
#    serializer_class = AppUsersSerializer
