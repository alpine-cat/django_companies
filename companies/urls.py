from django.urls import path
from . import views

urlpatterns = [
    path('', views.CompanyView.as_view(), name='companies_list'),
    path('<int:pk>/', views.CompanyDetailView.as_view(), name='details'),
    path('<int:pk>/manager',views.ManagerView.as_view(), name='manager_list'),
    path('<int:pk>/details/work-create',views.WorkCreateView.as_view(), name='create_work'),
    path('workers/', views.WorkerView.as_view(), name='worker_list'),
    path('workers/<int:pk>/', views.WorkerDetailsView.as_view(), name='worker_details'),
    path('workers/<int:pk>/detail/create',views.WorkTimeCreateView.as_view(), name='create_worktime'),
    path('company/<int:company_id>/details/<int:work_id>', views.SetWorkPlace.as_view(), name='set_worker')
]