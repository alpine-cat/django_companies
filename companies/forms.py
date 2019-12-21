from django import forms
from .models import WorkTime, Work, WorkPlace


class AddWorkTimeForm(forms.ModelForm):
    class Meta:
        model = WorkTime
        fields = ['worker', 'work_place', 'date_start', 'date_end']


class AddWorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ['company', 'work_name']
        

class SetWorkPlaceForm(forms.ModelForm):
    class Meta:
        model = WorkPlace
        fields = ['work', 'workplace_name', 'worker']
