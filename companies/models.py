from django.db import models
from django.utils.translation import gettext_lazy as _


STATUS_NEW = 0
STATUS_APPROVED = 1
STATUS_CANCELLED = 2
STATUS_FINISHED = 3


class Human(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

    class Meta:
        abstract = True


class Company(models.Model):
    company_name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.company_name)


class Manager(Human):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    email = models.CharField(max_length=100)


class Work(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    work_name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.work_name)


class Worker(Human):
    pass


class WorkPlace(models.Model):
    manager = models.OneToOneField(Manager, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    workplace_name = models.CharField(max_length=200)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    limit_time = models.IntegerField

    STATUSES = [
        (STATUS_NEW, _('New')),
        (STATUS_APPROVED, _('Approved')),
        (STATUS_CANCELLED, _('Cancelled')),
        (STATUS_FINISHED, _('Finished')),
    ]

    status = models.IntegerField(choices=STATUSES, default=STATUS_NEW)

    def __str__(self):
        return str(self.workplace_name)


class WorkTime(models.Model):
    STATUSES = [
        (STATUS_NEW, _('New')),
        (STATUS_APPROVED, _('Approved')),
        (STATUS_CANCELLED, _('Cancelled')),
    ]

    worker = models.ForeignKey(Worker, on_delete=models.PROTECT) 
    work_place = models.ForeignKey(WorkPlace, on_delete=models.CASCADE, related_name='work_times')
    status = models.IntegerField(choices=STATUSES, default=STATUS_NEW)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()

    def __str__(self):
        return str(self.work_place + _(' start:') + self.date_start + _(' end:') + self.date_end)


class Statistics(models.Model):
    date_of_create = models.DateField(auto_now_add=True)
    workplace = models.ForeignKey(WorkPlace, related_name='workplaces', on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, related_name='workers', on_delete=models.CASCADE)
    worked_time = models.FloatField()
