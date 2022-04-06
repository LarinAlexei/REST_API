from rest_framework.serializers import HyperlinkedModelSerializer
from authapp.models import ApiUser


class AppUsersSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ApiUser
        # fields = '__all__'
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'add_datetime', 'last_modified']
