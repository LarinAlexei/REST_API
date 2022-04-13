from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer
from authapp.serializers import AppUsersSerializer
from userworkapp.models import Project, UserWorkingProject, ToDo, Executor


class ProjectModelSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        extra_kwargs = {'user_on_project': {'required': False}}


class ProjectModelSerializer(serializers.ModelSerializer):
    user_on_project = serializers.StringRelatedField(many=True)

    class Meta:
        model = Project
        fields = '__all__'


class UserWorkingProjectSerializer(serializers.Serializer):
    project = serializers.StringRelatedField(many=False)
    # project = serializers.StringRelatedField(many=False)
    # user = AppUsersSerializer()

    class Meta:
        model = UserWorkingProject
        fields = '__all__'


class ExecutorToDoModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Executor
        fields = '__all__'


class TodoModelSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = '__all__'


class TodoModelSerializer(serializers.ModelSerializer):
    user_one_todo = serializers.StringRelatedField(many=True)
    # project = ProjectModelSerializer()

    class Meta:
        model = ToDo
        fields = '__all__'
