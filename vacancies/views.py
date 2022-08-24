from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, Resolver404
from django.views.generic import ListView, TemplateView, CreateView, UpdateView

from vacancies.forms import SendApplicationForm, MyCompanyForm, MyVacancyForm
from vacancies.models import Specialty, Vacancy, Company, Application
from vacancies.signals.send_application_signal import application_signal


class MainView(ListView):
    model = Specialty
    template_name = 'vacancies/index.html'
    context_object_name = 'specialties'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['companies'] = Company.objects.all()
        return context


class VacanciesView(ListView):
    model = Vacancy
    template_name = 'vacancies/vacancies.html'
    context_object_name = 'vacancies'  # это по сути object_list, то есть все объекты из модели Vacancy

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['specialties'] = Specialty.objects.all()
        return context


class VacancyTypeView(ListView):
    model = Vacancy
    template_name = 'vacancies/vacancies.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        specialty = get_object_or_404(Specialty, code=self.kwargs['vacancy_type'])
        context['specialties'] = [specialty]
        context['vacancies'] = Vacancy.objects.filter(specialty=specialty)
        return context


class CompanyView(TemplateView):
    model = Company
    template_name = 'vacancies/company.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        try:
            company = Company.objects.get(pk=self.kwargs['company_id'])
        except ObjectDoesNotExist:
            raise Http404("Компании с таким id не существует")
        vacancies_by_company = Vacancy.objects.filter(company=company.id)
        context['company'] = company
        context['vacancies'] = vacancies_by_company
        return context


class VacancyView(TemplateView):
    model = Vacancy
    template_name = 'vacancies/vacancy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        try:
            vacancy = Vacancy.objects.get(pk=self.kwargs['vacancy_id'])
        except ObjectDoesNotExist:
            raise Http404("Вакансии с таким id не существует")
        context['vacancy'] = vacancy
        context['form'] = SendApplicationForm
        return context

    def post(self, request, vacancy_id):
        try:
            vacancy = Vacancy.objects.get(pk=vacancy_id)
        except ObjectDoesNotExist:
            raise Http404("Вакансии с таким id не существует")
        if request.method == 'POST':
            send_application_form = SendApplicationForm(request.POST)
            if send_application_form.is_valid():
                application = send_application_form.save(commit=False)
                application.user = request.user
                application.vacancy = vacancy
                application.save()
                application_signal.send(sender=self.__class__)
                return redirect('application_sent', self.kwargs['vacancy_id'])
        else:
            send_application_form = SendApplicationForm()
        return render(request, 'vacancies/vacancy.html', context={'form': send_application_form,
                                                                  'vacancy': vacancy})


class SentView(TemplateView):
    template_name = 'vacancies/sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancy_id'] = self.kwargs['vacancy_id']
        return context


class MyCompanyLetsStartView(LoginRequiredMixin, TemplateView):
    template_name = 'vacancies/company-create.html'
    login_url = '/login/'


class MyCompanyCreateView(LoginRequiredMixin, CreateView):
    form_class = MyCompanyForm
    template_name = 'vacancies/company-edit.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = {
            'form': MyCompanyForm,
            'isCompanyClick': "nav-link active",
            'isVacancyClick': "nav-link"
        }
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            mycompany_form = MyCompanyForm(request.POST, request.FILES)
            if mycompany_form.is_valid():
                mycompany = mycompany_form.save(commit=False)
                mycompany.owner = request.user
                mycompany.save()
                messages.success(self.request, 'Компания успешно создана!')
                return redirect('mycompany')
        else:
            mycompany_form = MyCompanyForm()
        return render(request, 'vacancies/company-edit.html', context={'form': mycompany_form,
                                                                       'isCompanyClick': "nav-link active",
                                                                       'isVacancyClick': "nav-link",
                                                                       })


class MyCompanyFullView(LoginRequiredMixin, UpdateView):
    form_class = MyCompanyForm
    template_name = 'vacancies/company-edit.html'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        try:
            mycompany = Company.objects.get(owner=request.user)
        except ObjectDoesNotExist:
            return redirect('letsstart_mycompany')
        else:
            filled_form = MyCompanyForm(instance=mycompany)
            context = {
                'form': filled_form,
                'mycompany': mycompany,
                'isCompanyClick': "nav-link active",
                'isVacancyClick': "nav-link"
            }
            return render(request, 'vacancies/company-edit.html', context=context)

    def post(self, request, *args, **kwargs):
        try:
            mycompany = Company.objects.get(owner=request.user)
        except ObjectDoesNotExist:
            return redirect('letsstart_mycompany')
        if request.method == 'POST':
            mycompany_form = MyCompanyForm(request.POST, request.FILES, instance=mycompany)
            if mycompany_form.is_valid():
                mycompany = mycompany_form.save(commit=False)
                mycompany.owner = request.user
                mycompany.save()
                messages.success(self.request, 'Информация о компании успешно обновлена!')
                return redirect('mycompany')
        else:
            mycompany_form = MyCompanyForm(instance=mycompany)
        return render(request, 'vacancies/company-edit.html', context={'form': mycompany_form})


class MyCompanyVacanciesView(LoginRequiredMixin, ListView):
    model = Vacancy
    template_name = 'vacancies/vacancy-list.html'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        vacancies_by_company = None
        try:
            mycompany = Company.objects.get(owner=request.user)
            vacancies_by_company = Vacancy.objects.filter(company=mycompany.pk)
        except ObjectDoesNotExist:
            return redirect('letsstart_mycompany')
        context = {
            'mycompany': mycompany,
            'vacancies': vacancies_by_company,
            'isCompanyClick': "nav-link",
            'isVacancyClick': "nav-link active"
        }
        return render(request, 'vacancies/vacancy-list.html', context=context)


class MyCompanyCreateVacancyView(LoginRequiredMixin, CreateView):
    form_class = MyVacancyForm
    template_name = 'vacancies/vacancy-edit.html'
    success_url = reverse_lazy('home')
    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            myvacancy_form = MyVacancyForm(request.POST)
            if myvacancy_form.is_valid():
                myvacancy = myvacancy_form.save(commit=False)
                myvacancy.company = Company.objects.get(owner=request.user)
                myvacancy.save()
                return redirect('mycompany_vacancies')
        else:
            myvacancy_form = MyVacancyForm()
        return render(request, 'vacancies/vacancy-edit.html', context={'form': myvacancy_form})


class MyCompanyVacancyFullView(LoginRequiredMixin, UpdateView):
    form_class = MyVacancyForm
    template_name = 'vacancies/vacancy-edit.html'
    success_url = reverse_lazy('home')
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        try:
            Company.objects.get(owner=request.user)
        except ObjectDoesNotExist:
            return redirect('letsstart_mycompany')

        myvacancy = get_object_or_404(
            Vacancy.objects.filter(
                company__owner_id=request.user.pk
            ),
            pk=self.kwargs['vacancy_id'],
        )
        applications = Application.objects.filter(vacancy=self.kwargs['vacancy_id'])

        filled_form = MyVacancyForm(instance=myvacancy)
        context = {
            'applications': applications,
            'myvacancy': myvacancy,
            'form': filled_form,
        }
        return render(request, 'vacancies/vacancy-edit.html', context=context)

    def post(self, request, **kwargs):
        try:
            myvacancy = Vacancy.objects.get(pk=self.kwargs['vacancy_id'])
        except ObjectDoesNotExist:
            raise Http404('У вашей компании нет вакасии с таким id!')
        if request.method == 'POST':
            myvacancy_form = MyVacancyForm(request.POST, instance=myvacancy)
            if myvacancy_form.is_valid():
                myvacancy = myvacancy_form.save(commit=False)
                myvacancy.company = Company.objects.get(owner=request.user)
                myvacancy.save()
                return redirect('mycompany_vacancies')
        else:
            myvacancy_form = MyVacancyForm(instance=myvacancy)
        return render(request, 'vacancies/vacancy-edit.html', context={'form': myvacancy_form})


def custom_handler404(request, exception):
    if isinstance(exception, Resolver404):
        return HttpResponseNotFound("Запрашиваемая страница не найдена!")
    else:
        return HttpResponseNotFound(exception)


def custom_handler500(request):
    return HttpResponseServerError("Ошибка сервера!")
