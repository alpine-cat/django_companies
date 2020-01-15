from .models import Company, Work, Manager, Worker, WorkTime, WorkPlace

from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from .serializers import (
    ManagerSerializer, WorkerSerializer,WorkPlaceSerializer, WorkPlaceDetailSerializer,
    CompanySerializer, WorkSerializer, CompanyDetailSerializer, WorkTimeSerializer
)


class CompanyView(viewsets.ModelViewSet):
    queryset = Company.objects.all()

    def get_serializer_class(self):
        if self.action == 'create_manager':
            return ManagerSerializer
        elif self.action == 'create_work':
            return WorkSerializer
        elif self.action == 'retrieve':
            return CompanyDetailSerializer
        return CompanySerializer

    @action(methods=['post'], detail=True)
    def create_manager(self, request, pk=None):
        company = self.get_object()
        serializer = ManagerSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(company_name=company)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def create_work(self, request, pk=None):
        company = self.get_object()
        serializer = WorkSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(company=company)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ManagerView(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly,)


class WorkerView(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly,)


class WorkTimeView(viewsets.ModelViewSet):
    queryset = WorkTime.objects.all()
    serializer_class = WorkTimeSerializer
    permission_class = (permissions.IsAuthenticated,)


class WorkView(viewsets.ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly,)


class SetWorkPlace(viewsets.ModelViewSet):
    queryset = WorkPlace.objects.all()
    permissions_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return WorkPlaceDetailSerializer
        if self.action == 'create_worktime':
            return WorkTimeSerializer
        return WorkPlaceSerializer

    @action(methods=['post'], detail=True)
    def create_worktime(self, request, pk=None):
        wp = self.get_object()
        serializer = WorkTimeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(workplace=wp, work=wp.work_name,
                            worker=wp.worker_name)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
