from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer
from authapp.models import ApiUser


class AppUsersSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ApiUser
        # fields = '__all__'
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'add_datetime', 'last_modified']


class AppUsersExtendedSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ApiUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'add_datetime', 'last_modified', 'is_workers',
                  'is_superuser']


class ShortUserSerializer(ModelSerializer):
    class Meta:
        model = ApiUser
        fields = ['id', 'username', 'first_name', 'last_name']
