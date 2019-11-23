from django.db import models


class Company(models.Model):
    company_name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.company_name)

class Manager(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    manager_name = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.manager_name)

class Work(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    work_name = models.CharField(max_length=200)
    def __str__(self):
        return str(self.work_name)

class WorkPlace(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    workplace_name = models.CharField(max_length=200)
    def __str__(self):
        return str(self.workplace_name)

class Worker(models.Model):
    workplace = models.OneToOneField(WorkPlace, on_delete=models.CASCADE)
    worker_name = models.CharField(max_length=100)
    def __str__(self):
        return str(self.worker_name)
