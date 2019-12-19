from django.db import models

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
    
    

class Work(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    work_name = models.CharField(max_length=200)
    def __str__(self):
        return str(self.work_name)

class Worker(Human):
    pass

class WorkPlace(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    workplace_name = models.CharField(max_length=200)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)

    STATUS_NEW  = 0
    STATUS_APPROVED = 1
    STATUS_CANSELLED = 2
    STATUS_FINISHED = 3
    STATUSES = [
        (STATUS_NEW, 'New'), 
        (STATUS_APPROVED, 'Approved'),
        (STATUS_CANSELLED, 'Canselled'),
        (STATUS_FINISHED, 'Finished'),
    ]

    status = models.IntegerField(choices=STATUSES, default=STATUS_NEW)

    def __str__(self):
        return str(self.workplace_name)

class WorkTime(models.Model):
    STATUS_NEW  = 0
    STATUS_APPROVED = 1
    STATUS_CANSELLED = 2
    STATUSES = [
        (STATUS_NEW, 'New'), 
        (STATUS_APPROVED, 'Approved'),
        (STATUS_CANSELLED, 'Canselled'),
    ]

    worker = models.ForeignKey(Worker, on_delete=models.PROTECT) 
    work_place = models.ForeignKey(WorkPlace, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUSES, default=STATUS_NEW)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()

    def __str__(self):
        pass
