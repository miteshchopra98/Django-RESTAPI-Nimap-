from rest_framework import serializers
from django.contrib.auth.models import User
from app1.models import Client, Project
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    client = serializers.CharField(source='client.name', read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), write_only=True)
    user_ids = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, write_only=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'client', 'client_id', 'users', 'user_ids', 'created_at', 'created_by']
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None
        user_ids = validated_data.pop('user_ids')
        client = validated_data.pop('client_id')
        project = Project.objects.create(client=client, created_by=user ,**validated_data)
        project.users.set(user_ids)
        return project

class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'name', 'updated_at', 'created_at','created_by']
        

    def create(self, validated_data):
        name = validated_data.pop('name')
        request = self.context.get('request', None)
        user = request.user if request else None
        client = Client.objects.create(name = name,created_by=user, **validated_data)
        return client

class MyClientSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'name', 'projects', 'updated_at', 'created_at','created_by']