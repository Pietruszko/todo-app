from django.shortcuts import render
from .models import Task
from .serializers import TaskSerializer, UserSerializer
from .filters import TaskFilter
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()  # Default queryset (required for router)
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]