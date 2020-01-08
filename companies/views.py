from .models import Company, Work, Manager, Worker, WorkTime
from .forms import AddWorkForm, AddWorkTimeForm, SetWorkPlaceForm
from django.views import generic
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

import logging

logger = logging.getLogger('sentry_log')


class CompanyView(LoginRequiredMixin, generic.ListView):
    template_name = 'companies/index.html'
    context_object_name = 'companies_list'

    def get_queryset(self):
        return Company.objects.all()


class ManagerView(generic.ListView):
    model = Manager
    template_name = 'companies/managers.html'
    context_object_name = 'managers'

    def get_queryset(self):
        company = get_object_or_404(Company, id=self.kwargs.get('pk'))
        return Manager.objects.filter(company=company)


class CompanyDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'companies.can_view_company_detail'
    raise_exception = True

    model = Company
    template_name = 'companies/details.html'


class WorkerView(generic.ListView):
    model = Worker
    template_name = 'companies/workers.html'
    context_object_name = 'workers'


class WorkerDetailsView(generic.DetailView):
    model = Worker
    template_name = 'companies/worker_details.html'


class WorkCreateView(generic.CreateView):
    template_name = 'companies/create_work.html'
    form_class = AddWorkForm

    def get_success_url(self):
        company_id = self.kwargs.get('pk')
        return reverse('details', kwargs={'pk': company_id})

    def get_initial(self):
        company = get_object_or_404(Company, id=self.kwargs.get('pk'))
        return {'company': company}

    def form_valid(self, form):
        form.save()
        data = self.request.POST
        logger.debug(
            'company: %s, work name: %s',
            data['company'], data['work_name']
        )
        logger.info('work created')
        return super().form_valid(form)


class WorkTimeCreateView(generic.CreateView):
    form_class = AddWorkTimeForm
    template_name = 'companies/create_worktime.html'

    def get_success_url(self):
        worker_id = self.kwargs.get('pk')
        return reverse('worker_detail', kwargs={'pk': worker_id})

    def get_initial(self):
        worker = get_object_or_404(Worker, id=self.kwargs.get('pk'))
        return {'worker': worker}

    def form_valid(self, form):
        form.save()
        data = self.request.POST
        logger.debug('start: %s, end: %s, worker: %s, workplace:%s, status:%s',
                     data['date_start'], data['date_end'], data['worker'],
                     data['work_place'], data['status'])
        logger.info('work time created')
        return super().form_valid(form)


class SetWorkPlace(generic.CreateView):
    form_class = SetWorkPlaceForm
    template_name = 'companies/set_worker_to_workplace.html'

    def get_initial(self):
        work_name = get_object_or_404(Work, id=self.kwargs.get('work_id'))
        return {'work_name': work_name}

    def get_success_url(self):
        company_id = self.kwargs.get('company_id')
        return reverse('details', kwargs={'pk': company_id})

    def form_valid(self, form):
        form.save()
        data = self.request.POST
        logger.debug('worker: %s, work:%s',
                     data['worker'], data['work'])
        logger.info('set worker to workplace')
        return super().form_valid(form)
