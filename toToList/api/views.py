from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from rest_framework.decorators import api_view

from api.models import List, Task
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from django.views.decorators.csrf import csrf_exempt
import json
from api.serializers import TaskSerializer

MISSING_FIELDS_MSG = 'Missing obligatory fields: {}'
MISSING_QUERY_MSG = 'Missing obligatory query fields: {}'
OBJECT_DOES_NOT_EXIST_MSG = 'Object with provided id does not exist'

def _get_name_from_body(request: Request) -> str:
    # change to request.data
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    return body.get('name', '')

def list_all(request: Request) -> HttpResponse:
    lists = list(List.objects.all().values('name', 'id'))
    return HttpResponse(json.dumps(lists, indent=2), status=status.HTTP_200_OK)

@csrf_exempt
def list_create(request: Request) -> HttpResponse:
    name = _get_name_from_body(request)
    if not name:
        return HttpResponse(MISSING_FIELDS_MSG.format('name'), status=status.HTTP_400_BAD_REQUEST)
    list_obj = List(name=name)
    list_obj.save()
    return HttpResponse(list_obj.pk, status=status.HTTP_200_OK)

@csrf_exempt
def list_edit(request: Request, pk: int) -> HttpResponse:
    if not pk:
        return HttpResponse(MISSING_QUERY_MSG.format('id'), status=status.HTTP_400_BAD_REQUEST)
    name = _get_name_from_body(request)
    if not name:
        return HttpResponse(MISSING_FIELDS_MSG.format('name'), status=status.HTTP_400_BAD_REQUEST)
    try:
        list_obj = List.objects.get(pk=pk)
    except List.DoesNotExist:
        return HttpResponse(OBJECT_DOES_NOT_EXIST_MSG, status=status.HTTP_400_BAD_REQUEST)
    list_obj.name = name
    list_obj.save()
    return HttpResponse(list_obj.pk, status=status.HTTP_200_OK)

@csrf_exempt
def list_delete(request: Request, pk: int) -> HttpResponse:
    if not pk:
        return HttpResponse(MISSING_QUERY_MSG.format('id'), status=status.HTTP_400_BAD_REQUEST)
    try:
        list_obj = List.objects.get(pk=pk)
    except List.DoesNotExist:
        return HttpResponse(OBJECT_DOES_NOT_EXIST_MSG, status=status.HTTP_400_BAD_REQUEST)
    pk = list_obj.pk
    list_obj.delete()
    return HttpResponse(pk, status=status.HTTP_200_OK)


def list_get(request: Request, pk: int) -> HttpResponse:
    try:
        list_obj = List.objects.get(pk=pk)
    except List.DoesNotExist:
        return HttpResponse(OBJECT_DOES_NOT_EXIST_MSG, status=status.HTTP_400_BAD_REQUEST)
    return HttpResponse(json.dumps({'id': list_obj.id, 'name': list_obj.name}), status.HTTP_200_OK)


def task_all(request: Request, pk) -> HttpResponse:
    try:
        List.objects.get(pk=pk)
    except List.DoesNotExist:
        return HttpResponse(OBJECT_DOES_NOT_EXIST_MSG, status=status.HTTP_400_BAD_REQUEST)
    lists = list(Task.objects.filter(list=pk).values('title', 'description', 'list', 'id'))
    return HttpResponse(json.dumps(lists, indent=2), status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def task_create(request: Request) -> HttpResponse:
    task = TaskSerializer(data=request.data)
    if task.is_valid():
        task.save()
        return HttpResponse('Task created', status=status.HTTP_200_OK)
    else:
        return HttpResponse(str(task.errors), status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def task_edit(request: Request, pk: int) -> HttpResponse:
    task = Task.objects.get(pk=pk)
    edited_task = TaskSerializer(instance=task, data=request.data)
    if edited_task.is_valid():
        edited_task.save()
    else:
        return HttpResponse(str(edited_task.errors), status=status.HTTP_400_BAD_REQUEST)
    return HttpResponse('Task updated', status=status.HTTP_200_OK)

@api_view(['DELETE'])
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return HttpResponse('Task deleted', status=status.HTTP_200_OK)
