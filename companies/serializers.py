from rest_framework import serializers

from .models import Company, Manager, Work, Worker, WorkPlace, WorkTime


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    managers = serializers.StringRelatedField(many=True)
    works = serializers.StringRelatedField(many=True)

    class Meta:
        model = Company
        fields = ('url', 'id', 'company_name', 'managers', 'works')


class ManagerSerializer(serializers.HyperlinkedModelSerializer):
    company_name = serializers.ReadOnlyField(source='company.company_name')

    class Meta:
        model = Manager
        fields = ('url', 'id', 'name', 'company_name', 'company')


class WorkerSerializer(serializers.HyperlinkedModelSerializer):
    workplace = serializers.SerializerMethodField('work_place')

    def work_place(self, worker):
        if WorkPlace.objects.filter(worker=worker).exists():
            workplace = WorkPlace.objects.filter(worker=worker)
            return f'{workplace[0].workplace_name}'
        return 'Doesn`t work now'

    class Meta:
        model = Worker
        fields = ('url', 'id', 'name', 'workplace')


class WorkPlaceSerializer(serializers.HyperlinkedModelSerializer):
    work_name = serializers.ReadOnlyField(source='work.work_name')
    worker_name = serializers.ReadOnlyField(source='worker.name')

    class Meta:
        model = WorkPlace
        fields = ('url', 'workplace_name', 'work_name', 'worker_name', 'status',)


class WorkSerializer(serializers.HyperlinkedModelSerializer):
    company = serializers.ReadOnlyField(source='company.company_name')

    class Meta:
        model = Work
        fields = ('url', 'id', 'work_name', 'company')


class WorkTimeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WorkTime
        fields = ('id', 'date_start', 'date_end', 'status')


class CompanyDetailSerializer(serializers.HyperlinkedModelSerializer):
    managers = ManagerSerializer(many=True)
    works = WorkSerializer(many=True)

    class Meta:
        model = Company
        fields = ('url', 'id', 'company_name', 'managers', 'works')


class WorkPlaceDetailSerializer(serializers.HyperlinkedModelSerializer):
    work_name = WorkSerializer()
    worker_name = WorkerSerializer()
    worktimes = WorkTimeSerializer(read_only=True, many=True)

    class Meta:
        model = WorkPlace
        fields = ('id', 'name', 'work_name', 'worker_name', 'status', 'worktimes')


