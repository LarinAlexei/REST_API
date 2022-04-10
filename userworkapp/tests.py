from django.test import TestCase
import json
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient, APISimpleTestCase, APITestCase
from authapp.models import ApiUser
from userworkapp.models import Project, UserWorkingProject, Executor, ToDo
from userworkapp.views import ProjectViewSet, UserWorkingProjectViewSet, ToDoViewSet, ExecutorViewSet
from rest_framework.authtoken.models import Token
from userworkapp.serializers import ProjectModelSerializerBase
from mixer.backend.django import mixer
from django.contrib.auth import get_user_model
import pdb


# Create your tests here.


class TestProjectViewSet(TestCase):

    def setUp(self):
        self.data = {'name': 'test1',
                     'description': 'super'}
        self.user = ApiUser.objects.create_superuser(username='Alex', email='Alex32@mail.ru', password='geek')

    def test_get_projects_list(self):
        factory = APIRequestFactory()
        request = factory.get('/api/project/')
        view = ProjectViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_project(self):
        factory = APIRequestFactory()
        request = factory.post(path='/api/project/', data=self.data, format='json')
        view = ProjectViewSet.as_view({'post': 'create'})
        response = view(request)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_project_admin(self):
        factory = APIRequestFactory()
        request = factory.post(path='/api/project/',
                               data=self.data,
                               format='json')
        admin = ApiUser.objects.create_superuser(username='Larin', email='Larin@gmail.com',
                                                 password='geek', is_staff=True)
        view = ProjectViewSet.as_view({'post': 'create'})
        token_admin = Token.objects.create(user=admin)
        print(token_admin)
        force_authenticate(request, user=admin, token=f'Token {token_admin}')
        response = view(request)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_put_project_info(self):
        project = Project.objects.create(name='Test', description='Test project')

        project.user_on_project.add(self.user)
        client = APIClient()
        response = client.get(f'/api/projects/{project.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        users_on_project = UserWorkingProject.objects.filter(project=project)
        self.assertTrue(users_on_project.count() > 0)

        client.login(username=self.user.username, password='geek')
        response_put = client.put(f'/api/project/{project.id}/',
                                  {'name': 'Name Update',
                                   'description': 'info'})
        self.assertTrue(response_put.status_code, status.HTTP_200_OK)

        self.assertTrue(Project.objects.get(pk=project.id).name, 'Name Update')


class TestToDoViewSet(TestCase):
    def setUp(self):
        self.pwd = 'Larin'
        self.admin = ApiUser.objects.create_superuser('Larin', 'Larin@mail.ru', self.pwd)
        self.project = Project.objects.create(name='Project')
        self.project_id = self.project.id
        self.client_anon = APIClient()
        self.client = APIClient()

        self.client.login(username=self.admin.username, password=self.pwd)

    def test_get_todo(self):
        todo = mixer.blend(ToDo, project_id=self.project)
        response = self.client_anon.get(f'/api/todo/{todo.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client_anon.get(f'/api/todo/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_todo_anon(self):
        response = self.client_anon.post(f'/api/todo/', {'title': 'new_todo', 'project_id': self.project_id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_put_todo_admin(self):
        response = self.client.post(f'/api/todo/', {'title': 'new_todo', 'project_id': self.project_id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        todo = ToDo.objects.all()[0]
        response = self.client.put(f'/api/todo/{todo.id}/',
                                   {'title': 'update_todo',
                                    'project_id': self.project_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    class TestProjectViewSetAPITest(APITestCase):
        def setUp(self):
            self.admin = ApiUser.objects.create_superuser('Mark', 'Mark@gmail.ru', 'geek')
            self.client.login(username='Mark', password='geek')
            # self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_admin}')
            self.project = Project.objects.create(name='Оригинальный вид проекта', description='В редакции')
            self.data = ProjectModelSerializerBase(self.project).data
            self.data.update({'name': 'test3', 'description': 'super'})

        def test_get_projects(self):
            response = self.client.get('/api/project/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_post_projects(self):
            response = self.client.post('/api/project/',
                                        {'name': 'New project',
                                         'description': 'super'})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        def test_edit_delete_project(self):
            check_val = self.data['name']
            response = self.client.put(f'/api/project/{self.project.id}/', self.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            project = Project.objects.get(id=self.project.id)
            self.assertEqual(project.name, check_val)

            response = self.client.delete(f'/api/projects/{self.project.id}/')
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
