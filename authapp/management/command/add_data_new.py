from django.core.management.base import BaseCommand, CommandError
from authapp.models import ApiUser
from userworkapp.models import Project, UserWorkingProject, ToDo, Executor
from uuid import uuid4
from faker import Faker


class Command(BaseCommand):

    def handle(self, *args, **options):
        users = ApiUser.objects.all()
        faker = Faker()

        for i in range(20):
            project = Project(name=f'Проект № {i} ({uuid4()})',
                              description=f'Описание проекта №{1}',
                              href_repo=f'https://www.test.com/project_{i}')
            project.save()
            project.user_on_project.add(users[0])
            project.save()

            for j in range(5):
                todo = ToDo(title=f'{faker.text(max_nb_chars=20)}', description=f'{faker.sentence(nb_words=10)}',
                            project_id=project)
                todo.save()
                users_on_project = UserWorkingProject.objects.filter(project=project)
                todo.save()
                todo.user_on_todo.add(users_on_project[0])
