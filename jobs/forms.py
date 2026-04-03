from django import forms
from .models import Job, JobApplication, JOB_CATEGORIES
from accounts.models import REGIONS


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'category', 'salary', 'salary_type',
                  'region', 'address', 'lat', 'lng', 'image', 'workers_needed',
                  'work_date', 'status']
        labels = {
            'title': 'Ish nomi',
            'description': 'Ish tavsifi',
            'category': 'Kategoriya',
            'salary': 'To\'lov miqdori (so\'mda)',
            'salary_type': 'To\'lov turi',
            'region': 'Viloyat',
            'address': 'Manzil',
            'lat': '',
            'lng': '',
            'image': 'Rasm (ixtiyoriy)',
            'workers_needed': 'Nechta ishchi kerak',
            'work_date': 'Ish sanasi',
            'status': 'Holat',
        }
        widgets = {
            'lat': forms.HiddenInput(),
            'lng': forms.HiddenInput(),
            'work_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['message']
        labels = {'message': 'Qo\'shimcha xabar (ixtiyoriy)'}
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'O\'zingiz haqingizda qisqacha yozing...'})
        }
