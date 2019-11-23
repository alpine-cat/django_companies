from django.shortcuts import render
from django.http import Http404
from .models import Company, Work
from django.views import generic

class IndexView(generic.ListView):
    template_name = 'companies/index.html'
    context_object_name = 'companies_list'

    def get_queryset(self):
        return Company.objects.all()


class DetailView(generic.DetailView):
    model = Company
    template_name= 'companies/details.html'


def work_details(request, company_id, work_id):
    try:
        company =  Company.objects.get(id=company_id)
        work = company.work_set.get(id=work_id)
    except Work.DoesNotExist:
        raise Http404("Work does not exist")
    return render(request, 'companies/work_details.html', {'company':company, 'work':work})