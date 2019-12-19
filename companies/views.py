from django.shortcuts import render
from django.http import Http404
from .models import Company, Work, Manager, Worker, WorkTime
from .forms import AddWorkForm, AddWorkTimeForm, SetWorkPlaceForm
from django.views import generic
from django.shortcuts import get_object_or_404
from django.urls import reverse


class CompanyView(generic.ListView):
    template_name = 'companies/index.html'
    context_object_name = 'companies_list'

    def get_queryset(self):
        return Company.objects.all()


class ManagerView(generic.ListView):
    model = Manager
    template_name = 'polls/managers.html'
    context_object_name = 'managers'

    def get_queryset(self):
        company = get_object_or_404(Company, id=self.kwargs.get('pk'))
        return Manager.objects.filter(company=company)


class CompanyDetailView(generic.DetailView):
    model = Company
    template_name= 'companies/details.html'

class WorkerView(generic.ListView):
    model = Worker
    template_name = ''
    context_object_name = 'workers'

class WorkerDetailsView(generic.DetailView):
    model = Worker
    template_name = ''

    def get_queryset(self):
        context = super().get_context_data(**kwargs)
        worker = get_object_or_404(Worker, pk=self.kwargs.get('pk'))
        context['worktimes'] = WorkTime.objects.filter(worker=worker)
        return context


class WorkCreateView(generic.CreateView):
    template_name = 'companies/create_work.html'
    form_class = AddWorkForm

    def get_success_url(self):
        company_id = self.kwargs.get('pk')
        return reverse('company_detail', kwargs={'pk': company_id})

    def get_initial(self):
        company = get_object_or_404(Company, id=self.kwargs.get('pk'))
        return {'company': company}


class WorkTimeCreateView(generic.CreateView):
    form_class = AddWorkTimeForm
    template_name = 'companies/create_worktime.html'

    def get_success_url(self):
        worker_id = self.kwargs.get('pk')
        return reverse('worker_detail', kwargs={'pk': worker_id})

    def get_initial(self):
        worker = get_object_or_404(Worker, id=self.kwargs.get('pk'))
        return {'worker': worker}


class SetWorkPlace(generic.CreateView):
    form_class = SetWorkPlaceForm
    template_name = 'companies/set_worker_to_workplace.html'

    def get_initial(self):
        work_name = get_object_or_404(Work, id=self.kwargs.get('work_id'))
        return {'work_name': work_name}

    def get_success_url(self):
        company_id = self.kwargs.get('company_id')
        return reverse('company_details', kwargs={'pk': company_id})
