from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from app1.models import Client,Project
from app1.api.serializers import  ClientSerializer, MyClientSerializer, ProjectSerializer

# Create your views here.

def Home(request):
    return HttpResponse('This is Home page')

@api_view(['GET', 'POST'])
def client_list(request):
    
    if request.method == 'GET':
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)         
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ClientSerializer(data=request.data,  context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    

@api_view(['GET', 'PUT', 'DELETE'])                                                 
def client_details(request, pk):
    
    if request.method == 'GET':
        client = Client.objects.get(pk=pk)
        #projects = Project.objects.get(pk=pk)
        serializer = MyClientSerializer(client)
        return Response(serializer.data)

    if request.method == 'PUT':
        client = Client.objects.get(pk=pk)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    if request.method == 'DELETE':
        client = Client.objects.get(pk=pk)
        client.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def project_list(request):
    
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)         
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ProjectSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    

@api_view(['GET', 'PUT', 'DELETE'])                                                 
def project_details(request, pk):
    
    if request.method == 'GET':
        project = Project.objects.get(pk=pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    if request.method == 'PUT':
        project = Project.objects.get(pk=pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    if request.method == 'DELETE':
        project = Project.objects.get(pk=pk)
        project.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def my_projects(request):
    myprojects = Project.objects.filter(users=request.user)
    serializer = ProjectSerializer(myprojects, many=True)
    return Response(serializer.data)