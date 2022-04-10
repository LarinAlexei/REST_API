from django.shortcuts import render
from rest_framework import mixins, status, permissions
from userworkapp.models import Project, UserWorkingProject, ToDo, Executor
from rest_framework.viewsets import ModelViewSet
from userworkapp.serializers import ProjectModelSerializer, UserWorkingProjectSerializer, ExecutorToDoModelSerializer, \
    TodoModelSerializer, ProjectModelSerializerBase, TodoModelSerializerBase

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .models import Project, ToDo, UserWorkingProject, Executor
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.pagination import LimitOffsetPagination
from userworkapp.filters import ProjectFilter


# Create your views here.


class ProjectLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    # serializer_class = ProjectModelSerializer
    filters_class = ProjectFilter
    pagination_class = ProjectLimitOffsetPagination
    # permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ProjectModelSerializer
        return ProjectModelSerializerBase


class UserWorkingProjectViewSet(ModelViewSet):
    queryset = UserWorkingProject.objects.all()
    serializer_class = UserWorkingProjectSerializer


class ExecutorViewSet(ModelViewSet):
    queryset = Executor.objects.all()
    serializer_class = ExecutorToDoModelSerializer


class ToDoLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20


class ToDoViewSet(ModelViewSet):
    renderer_classes = [JSONRenderer]
    queryset = ToDo.objects.all()
    # serializer_class = TodoModelSerializer
    filters_fields = ['project_id']
    pagination_class = ToDoLimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return TodoModelSerializer
        return TodoModelSerializerBase

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        serializer = self.get_serializer(instance)
        if serializer:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.is_close = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
