from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import mixins, status, permissions
from userworkapp.models import Project, UserWorkingProject, ToDo, Executor
from rest_framework.viewsets import ModelViewSet
from userworkapp.serializers import ProjectModelSerializer, UserWorkingProjectSerializer, ExecutorToDoModelSerializer, \
    TodoModelSerializer, ProjectModelSerializerBase, TodoModelSerializerBase

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .models import Project, ToDo, UserWorkingProject, Executor, ApiUser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.pagination import LimitOffsetPagination
from userworkapp.filters import ProjectFilter


# Create your views here.


class ProjectLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 55


class ProjectViewSet(ModelViewSet):
    # queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer
    filterset_fields = ['name']
    filters_class = ProjectFilter
    # pagination_class = ProjectLimitOffsetPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        print(self.request.query_params)
        if self.request.query_params:
            search_char = self.request.query_params['search']
            queryset = Project.objects.filter(name__icontains=search_char)
        else:
            queryset = Project.objects.all()
        print(queryset)
        return queryset

    def create(self, request, *args, **kwargs):
        new_response = super(ProjectViewSet, self).create(request, *args, **kwargs)
        project = Project.objects.get(id=new_response.data['id'])
        users_id_on_project = request.data['user_on_project']
        if users_id_on_project:
            for user_id in users_id_on_project:
                user = ApiUser.objects.get(id=user_id['id'])
                project.user_on_project.add(user)
        project_serializer = ProjectModelSerializer(project)
        new_response.data = project_serializer.data
        print(project_serializer.data)
        return new_response

    def update(self, request, *args, **kwargs):
        new_response = super(ProjectViewSet, self).update(request, *args, **kwargs)
        print(new_response)

        project = Project.objects.get(id=new_response.data['id'])

        user_on_project_from_bd = UserWorkingProject.objects.filter(project_id=project.id)

        print(user_on_project_from_bd.values('id', 'user_id'))
        users_id_on_project_bd = list(map(lambda x: x['user_id'],
                                          user_on_project_from_bd.values('id', 'user_id')))

        print(request.data['user_on_project'])
        users_id_from_request = list(map(lambda x: int(x['id']), request.data['user_on_project']))

        users_id_list_for_delete = list(set(users_id_on_project_bd) - set(users_id_from_request))
        user_on_project_from_bd.filter(user_id__in=users_id_list_for_delete).delete()

        users_id_list_for_add = list(set(users_id_from_request) - set(users_id_on_project_bd))
        users = ApiUser.objects.filter(id__in=users_id_list_for_add)
        project.user_on_project.add(*users)

        project_serializer = ProjectModelSerializer(project)
        new_response.data = project_serializer.data
        print(project_serializer.data)
        return new_response

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProjectModelSerializer
        return ProjectModelSerializerBase


class UserWorkingProjectViewSet(ModelViewSet):
    queryset = UserWorkingProject.objects.all()
    serializer_class = UserWorkingProjectSerializer


class ExecutorViewSet(ModelViewSet):
    queryset = Executor.objects.all()
    serializer_class = ExecutorToDoModelSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated]


class ToDoLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 55


class ToDoViewSetBase(ModelViewSet):
    renderer_classes = [JSONRenderer]
    queryset = ToDo.objects.all()
    serializer_class = TodoModelSerializer


class ToDoViewSet(ModelViewSet):
    # renderer_classes = [JSONRenderer]
    queryset = ToDo.objects.all()
    # serializer_class = TodoModelSerializer
    filters_fields = ['project_id']
    pagination_class = ToDoLimitOffsetPagination

    def create(self, request, *args, **kwargs):
        new_response = super(ToDoViewSet, self).create(request, *args, **kwargs)
        print(request.data)
        print(new_response.data)
        # project = Project.objects.get(id=new_response.data['project_id'])
        new_todo = ToDo.objects.get(id=new_response.data['id'])
        users_on_todo_id_list = list(map(lambda i: int(i['id']), request.data['user_on_todo']))
        new_todo.user_on_todo.add(*users_on_todo_id_list)
        todo_serializer = TodoModelSerializer(new_todo)
        new_response.data = todo_serializer.data
        return new_response

    def update(self, request, *args, **kwargs):
        new_response = super(ToDoViewSet, self).update(request, *args, **kwargs)
        print(request.data)

        todo = ToDo.objects.get(id=new_response.data['id'])
        users_on_todo_from_bd = Executor.objects.filter(todo_id=todo.id)

        print(users_on_todo_from_bd.values('id', 'user_on_project_id'))
        users_on_todo_id_from_bd = list(map(lambda x: x['user_on_project_id'],
                                            users_on_todo_from_bd.values('id', 'user_on_project_id')))

        print(request.data['user_on_todo'])
        users_id_from_request = list(map(lambda x: int(x['id']), request.data['user_on_todo']))

        users_id_list_for_delete = list(set(users_on_todo_id_from_bd) - set(users_id_from_request))
        users_on_todo_from_bd.filter(user_on_project_id__in=users_id_list_for_delete).delete()

        users_id_list_for_add = list(set(users_id_from_request) - set(users_on_todo_id_from_bd))
        users_on_project = UserWorkingProject.objects.filter(id__in=users_id_list_for_add)
        todo.user_on_todo.add(*users_on_project)

        project_serializer = TodoModelSerializerBase(todo)
        new_response.data = project_serializer.data
        print(project_serializer.data)
        print(new_response.data)
        return new_response

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


class UserOnProjectViewSet(ModelViewSet):
    queryset = UserWorkingProject.objects.all()
    serializer_class = UserWorkingProjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserOnProjectById(ModelViewSet):
    # queryset = UserOnProject.objects.all()
    serializer_class = UserWorkingProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        print(self.request.query_params)
        project_id = int(self.request.query_params['project_id'])
        print(project_id)
        users_on_project = UserWorkingProject.objects.filter(project_id=project_id)
        print(users_on_project)
        return users_on_project


class SwaggerTemplateView(TemplateView):
    template_name = 'swagger-ui.html'
    extra_context = {'schema_url': 'openapi-schema'}


class RedocTemplateView(TemplateView):
    template_name = 'redoc.html'
    extra_context = {'schema_url': 'openapi-schema'}
