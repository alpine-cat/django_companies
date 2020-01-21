from company_dj.celery_app import app
import requests
from .models import Worker, WorkPlace, STATUS_APPROVED, Statistics
from django.utils import timezone
from django.core.mail import send_mail


@app.task(name='companies.tasks.set_workers')
def set_workers():
    resp = requests.get('https://jsonplaceholder.typicode.com/users')
    workers = resp.json()
    for worker in workers:
        Worker.objects.create(name=worker['name'])
    return Worker.objects.all()


@app.task(name='companies.tasks.set_statistics')
def set_statistics():
    approved_wp = WorkPlace.objects.filter(status=STATUS_APPROVED)
    week_ago_date = timezone.now() - timezone.timedelta(days=7)

    for work_place in approved_wp:
        result_time = 0
        if work_place.work_times.filter(date__gte=week_ago_date).exists():
            work_times = work_place.work_times.filter(date__gte=week_ago_date)
            for work_time in work_times:
                start = work_time.date_start.hour + work_time.date_start.minute / 60
                end = work_time.date_end.hour + work_time.date_end.minute / 60

                result_time += end - start

            Statistics.objects.create(workplace=work_place, worker=work_place.worker, worked_time=result_time)
            if result_time > work_place.limit_time:
                email = work_place.manager.email
                worker_name = work_place.worker.name
                hours_limit = result_time - work_place.limit_time
                app.send_task('email_send', args=[worker_name, hours_limit, email])


@app.task(name='companies.tasks.email_send')
def email_send(worker_name, hours_limit, email):
    send_mail(
        subject=f'Limit of hours exceeded',
        message=f'Worker {worker_name} exceeded the limit of hours: {hours_limit}',
        from_email='someemail@gmail.com',
        recipient_list=(email, ),
        fail_silently=False
    )
