from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'companies', views.CompanyView)
router.register(r'managers', views.ManagerView)
router.register(r'worker', views.WorkerView)
router.register(r'works', views.WorkView)
router.register(r'work-place', views.SetWorkPlace)