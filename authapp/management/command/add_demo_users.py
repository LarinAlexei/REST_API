from django.core.management.base import BaseCommand, CommandError
from authapp.models import ApiUser
from uuid import uuid4


# Создадим супер_пользователя

def create_user(username, password, email="", firstName="", lastName="", is_superuser=False):
    try:
        user = ApiUser(username=username, email=email, first_name=firstName, last_name=lastName)
        user.set_password(password)
        user.uid = uuid4()
        user.is_superuser = is_superuser
        user.is_staff = False
        user.save()
        return user
    except Exception as exc:
        print('Суперпользователь ранее был уже создан.', exc)


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        create_user('Larin', 'geek', 'Larin@mail.ru', 'Alex', 'L.A', is_superuser=True)
        create_user('Liza', 'geek', 'Liza@list.ru', 'Larina', 'LL')
        create_user('Mark', 'geek', 'Mark@mail.ru', 'Mark', 'ML')
