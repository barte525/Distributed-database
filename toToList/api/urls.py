from django.urls import path

from . import views

urlpatterns = [
    path('list', views.list_all, name='list_all'),
    path('list/create', views.list_create, name='list_create'),
    path('list/edit/<int:pk>', views.list_edit, name='list_edit'),
    path('list/delete/<int:pk>', views.list_delete, name='list_delete'),
    path('list/<int:pk>', views.list_get, name='list_get'),
    path('task/list/<int:pk>', views.task_all, name='task_all'),
    path('task/create', views.task_create, name='task_create'),
    path('task/edit/<int:pk>', views.task_edit, name='task_edit'),
    path('task/delete/<int:pk>', views.task_delete, name='task_delete'),
]