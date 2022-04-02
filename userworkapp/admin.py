from django.contrib import admin
from userworkapp.models import Project, UserWorkingProject, ToDo, Executor

# Register your models here.


admin.site.register(Project)
admin.site.register(UserWorkingProject)
admin.site.register(ToDo)
admin.site.register(Executor)
