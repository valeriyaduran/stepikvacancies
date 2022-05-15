from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import Application, Company, Vacancy


class SendApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['written_username', 'written_phone', 'written_cover_letter']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Отозваться на вакансию')),


class MyCompanyForm(forms.ModelForm):
    name = forms.CharField(label='Название компании')
    location = forms.CharField(label='География')
    logo = forms.ImageField(label='Логотип')
    employee_count = forms.IntegerField(label='Количество человек в компании')
    description = forms.CharField(label='Информация о компании', widget=forms.Textarea())

    class Meta:
        model = Company
        fields = ['name', 'location', 'logo', 'employee_count', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('save', 'Сохранить'))


class MyVacancyForm(forms.ModelForm):

    class Meta:
        model = Vacancy
        fields = ['title', 'specialty', 'salary_min', 'salary_max', 'skills', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('save', 'Сохранить'))
