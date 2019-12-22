from django.test import TestCase

from companies.models import Company, Manager, WorkPlace, Work, Worker


class TestManagerModel(TestCase):
    def setUp(self):
        self.company = Company.objects.create(company_name="Name")
        self.manager = Manager.objects.create(
            name="Manager1",
            company=self.company
        )

    def test_worker(self):
        self.assertIsNotNone(self.manager)
        self.assertEqual(self.manager.name, 'Manager1')


class TestCompanyModel(TestCase):
    def test_company(self):
        company = Company(company_name='Name')
        self.assertIsNotNone(company)


class TestWorkPlaceModel(TestCase):
    def setUp(self):
        company = Company(company_name='Name')
        worker = Worker(name='Worker')
        work = Work(
            company=company,
            work_name='WorkName',
        )

        self.wp = WorkPlace(
            worker=worker,
            work=work,
            workplace_name='new workplace',
        )

    def test_work_place(self):
        self.assertEqual(self.wp.status, 0)