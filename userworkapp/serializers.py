from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer
from authapp.serializers import AppUsersSerializer
from userworkapp.models import Project, UserWorkingProject, ToDo, Executor


class ProjectModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class UserWorkingProjectSerializer(serializers.ModelSerializer):
    # project = ProjectModelSerializer()
    # user = AppUsersSerializer()
    class Meta:
        model = UserWorkingProject
        fields = '__all__'


class ExecutorToDoModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Executor
        fields = '__all__'


class TodoModelSerializer(serializers.ModelSerializer):
    # project = ProjectModelSerializer()
    class Meta:
        model = ToDo
        fields = '__all__'
