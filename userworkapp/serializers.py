from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer
from authapp.serializers import AppUsersSerializer, ShortUserSerializer
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


class ProjectModelSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name']


class UserWorkingProjectSerializer(serializers.Serializer):
    project = serializers.StringRelatedField(many=False)
    # project = serializers.StringRelatedField(many=False)
    user = ShortUserSerializer()

    class Meta:
        model = UserWorkingProject
        fields = '__all__'


class UserOnProjectSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = UserWorkingProject
        fields = ['id', 'user']


class UserOnProjectSerializerShort(serializers.ModelSerializer):
    user = ShortUserSerializer()

    # project = ProjectSerializerBase()

    class Meta:
        model = UserWorkingProject
        fields = '__all__'


class ExecutorToDoModelSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = Executor
        fields = '__all__'


class ExecutorToDoModelSerializer(serializers.ModelSerializer):
    user_on_project = UserOnProjectSerializerBase()

    class Meta:
        model = Executor
        fields = '__all__'


class TodoModelSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = '__all__'


class TodoModelSerializer(serializers.ModelSerializer):
    project_id = ProjectModelSerializerShort()
    user_one_todo = serializers.StringRelatedField(many=True)

    # project = ProjectModelSerializer()

    class Meta:
        model = ToDo
        fields = '__all__'
