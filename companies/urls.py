from . import views

from django.urls import path


urlpatterns = [
    path('companies/', views.CompanyView.as_view(), name='companies_list'),
    path('companies/<int:pk>/', views.CompanyDetailView.as_view(), name='details'),
    path('companies/<int:pk>/manager', views.ManagerView.as_view(), name='manager_list'),
    path('companies/<int:pk>/work-create', views.WorkCreateView.as_view(), name='create_work'),
    path('workers/', views.WorkerView.as_view(), name='worker_list'),
    path('workers/<int:pk>/', views.WorkerDetailsView.as_view(), name='worker_details'),
    path('workers/<int:pk>/create', views.WorkTimeCreateView.as_view(), name='create_worktime'),
    path('company/<int:company_id>/<int:work_id>', views.SetWorkPlace.as_view(), name='set_worker'),
]