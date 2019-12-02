from django.contrib import admin

from .models import Company, Manager, Worker, Work, WorkPlace, WorkTime

admin.site.register(Company)
admin.site.register(Manager)
admin.site.register(Work)
admin.site.register(WorkPlace)
admin.site.register(Worker)
admin.site.register(WorkTime)