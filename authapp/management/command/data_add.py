from django.core.management.base import BaseCommand, CommandError
from authapp.models import ApiUser
from userworkapp.models import Project, UserWorkingProject, ToDo, Executor
from random import random
from uuid import uuid4


def add_project(name, description, customer, link_repo='n/a'):
    project = Project(name=name, description=description, customer_project=customer, link_repo=link_repo)
    project.save()
    return project


def add_working_user(project, user):
    user_working_project = UserWorkingProject(project_id=project.pk, user_id=user.pk)
    user_working_project.save()


def add_todo(project, title='n/a', description='n/a'):
    todo = ToDo(project_id=project.pk, title=title, description=description)
    todo.save()
    return todo


def add_executor(todo, user):
    executor = Executor(todo=todo, user_working_project=user)
    executor.save()


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        users = ApiUser.objects.all()
        for i in range(10):
            project = add_project(name=f'Новый заказ на проект {round(random() * 100)}',
                                  description='Что-то интересное',
                                  customer=users[round(random() * (len(users) - 1) + 1) - 1])
            for user in users[:round(random() * len(users))]:
                add_working_user(project, user)

            add_working_user = UserWorkingProject.objects.filter(project_id=project)
            print(add_working_user)

            for i in range(int(random() * 10)):
                todo = add_todo(project)
                add_executor(todo, add_working_user[round(random() * (len(add_working_user) - 1) + 1) - 1])
