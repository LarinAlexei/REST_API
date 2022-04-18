import graphene
from graphene_django import DjangoObjectType
from userworkapp.models import Project, ToDo, UserWorkingProject, Executor
from authapp.models import ApiUser
from django.db.models import Q
from datetime import datetime, timedelta


class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = '__all__'


class ToDoType(DjangoObjectType):
    class Meta:
        model = ToDo
        fields = '__all__'


class ExecutorType(DjangoObjectType):
    class Meta:
        model = Executor
        fields = '__all__'


class UserWorkingProjectType(DjangoObjectType):
    class Meta:
        model = UserWorkingProject
        fields = '__all__'


class UsersType(DjangoObjectType):
    class Meta:
        model = ApiUser
        fields = '__all__'


class ToDoStatusMutation(graphene.Mutation):
    '''Изменим статус ToDo'''

    class Cause:
        is_active = graphene.Boolean(required=True)
        is_close = graphene.Boolean(required=True)
        id = graphene.ID()

    todo = graphene.Field(ToDoType)

    @classmethod
    def mutate(cls, root, is_active, is_close, info, id):
        todo = ToDo.objects.get(pk=id)
        todo.is_active = is_active
        todo.is_close = is_close
        todo.save()
        return ToDoStatusMutation(todo=todo)


class AddTodoExecutorMutation(graphene.Mutation):
    '''Добавим пользователя в ToDo'''

    class Cause:
        user_id = graphene.Int(required=True)
        id = graphene.ID()

    todo = graphene.Field(ToDoType)

    @classmethod
    def mutate(cls, root, user_id, id, info):
        todo = ToDo.objects.get(id=id)
        project = todo.project_id
        user = ApiUser.objects.get(id=user_id)
        try:
            user = project.user_on_project.get(id=user.id)
        except:
            user = project.user_on_project.add(user)
        user_on_project = UserWorkingProject.objects.get(project=project, user=user)
        todo.user_on_project.add(user_on_project)
        return AddTodoExecutorMutation(todo=todo)


class Query(graphene.ObjectType):
    all_projects = graphene.List(ProjectType)
    all_todo = graphene.List(ToDoType)
    all_user = graphene.List(UsersType)
    user_on_project = graphene.List(UserWorkingProjectType)
    project_name_or_id = graphene.Field(ProjectType, id=graphene.Int(required=True),
                                        name=graphene.String(required=True))
    project_name_contains = graphene.List(ProjectType, name=graphene.String(required=True))
    user_search = graphene.List(UsersType, search_text=graphene.String(required=True))
    todo_term = graphene.List(ToDoType, from_days=graphene.Int(required=True))

    def resolve_all_projects(root, info):
        return Project.objects.all()

    def resolve_all_todo(root, info):
        return ToDo.objects.all()

    def resolve_all_user(root, info):
        return ApiUser.objects.all()

    def resolve_user_on_project(root, info):
        return UserWorkingProject.objects.all()

    def resolve_executor(root, info):
        return Executor.objects.all()

    def resolve_project_name_or_id(self, info, id=None, name=None):
        try:
            if id > 0:
                return Project.objects.get(id=id)
            elif name:
                return Project.objects.get(name=name)
        except Project.DoesNotExist:
            return None

    def resolve_project_name_contains(self, info, name=None):
        return Project.objects.filter(name__contains=name) if name else None

    def resolve_user_search(self, info, search_text):
        return ApiUser.objects.filter(Q(username__contains=search_text) | Q(first_name__contains=search_text) | Q(
            last_name__contains=search_text))

    def resolve_todo_term(self, info, from_days=5):
        term_date = datetime.combine(datetime.now().date() + timedelta(days=from_days), datetime.min.time())
        print(term_date)
        return ToDo.objects.filter(is_close=False, is_active=True, scheduled_date__lte=term_date).order_by(
            '-scheduled_date')


class Mutation(graphene.ObjectType):
    status_update_todo = ToDoStatusMutation.Field()
    add_user_on_todo = AddTodoExecutorMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
