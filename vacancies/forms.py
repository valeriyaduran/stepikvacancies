from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Application, User, Company, Vacancy


class SendApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['written_username', 'written_phone', 'written_cover_letter']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Отозваться на вакансию'))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('register', 'Зарегистрироваться'))


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('enter', 'Войти'))


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
    title = forms.CharField(label='Название вакансии')
    # specialty = forms.CharField(label='Специализация')
    skills = forms.CharField(label='Требуемые навыки', widget=forms.Textarea())
    salary_min = forms.IntegerField(label='Зарплата от')
    salary_max = forms.IntegerField(label='Зарплата до')
    description = forms.CharField(label='Описание вакансии', widget=forms.Textarea())

    class Meta:
        model = Vacancy
        fields = ['title', 'specialty', 'salary_min', 'salary_max', 'skills', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('save', 'Сохранить'))
