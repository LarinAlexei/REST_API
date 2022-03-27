from django.db import models
from uuid import uuid4
from authapp.models import ApiUser


# Create your models here.


class Project(models.Model):
    name = models.CharField(verbose_name='Название выполняемого проекта', max_length=256, blank=False, unique=True)
    description = models.TextField(verbose_name='Что входит в проект')
    link_repo = models.URLField(verbose_name='Ссылка на репозиторий проекта')
    customer_project = models.ForeignKey(ApiUser, on_delete=models.SET('n/a'), verbose_name='uid заказчика проекта')
    add_date = models.DateTimeField(verbose_name='Дата добавления проекта', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name='Дата последнего изменения', auto_now=True)

    def __str__(self):
        return self.name


class UserWorkingProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(ApiUser, on_delete=models.SET_NULL, null=True)
    add_date = models.DateTimeField(verbose_name='Дата добавления проекта', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name='Дата последнего изменения', auto_now=True)

    def __str__(self):
        return f"{self.user}"


class ToDo(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    #    customer_todo = models.ForeignKey(ApiUser, on_delete=models.SET_NULL, null=True,
    #    verbose_name = 'uid заказчик заметки')
    title = models.CharField(verbose_name='Заметка', max_length=64, unique=False, default='Не определена')
    description = models.TextField(verbose_name='Текст заметки', default='Не определен')
    is_active = models.BooleanField(verbose_name='Статус заметки', default=True)
    is_close = models.BooleanField(verbose_name='закрыто', default=False)
    scheduled_date = models.DateTimeField(verbose_name='Примерная дата завершения')
    actual_date = models.DateTimeField(verbose_name='Фактическая дата завершения')
    add_date = models.DateTimeField(verbose_name='Дата добавления проекта', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name='Дата последнего изменения', auto_now=True)


def __str__(self):
    return f"{self.project} - {self.title}"


class Executor(models.Model):
    todo = models.ForeignKey(ToDo, on_delete=models.CASCADE)
    user_working_project = models.ForeignKey(UserWorkingProject, on_delete=models.SET_NULL, null=True)
    add_date = models.DateTimeField(verbose_name='Дата добавления проекта', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name='Дата последнего изменения', auto_now=True)
