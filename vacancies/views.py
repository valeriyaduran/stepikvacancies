from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView, CreateView, UpdateView

from vacancies.forms import SendApplicationForm, UserRegisterForm, UserLoginForm, MyCompanyForm, MyVacancyForm
from vacancies.models import Specialty, Vacancy, Company, Application


class MainView(ListView):
    model = Specialty
    template_name = 'vacancies/index.html'
    context_object_name = 'specialties'
    extra_context = {'companies': Company.objects.all()}


class VacanciesView(ListView):
    model = Vacancy
    template_name = 'vacancies/vacancies.html'
    context_object_name = 'vacancies'  # это по сути object_list, то есть все объекты из модели Vacancy
    extra_context = {'specialties': Specialty.objects.all()}


class VacancyTypeView(ListView):
    model = Vacancy
    template_name = 'vacancies/vacancy-type.html'
    context_object_name = 'vacancies_by_specialty'

    def get_queryset(self):
        specialty = get_object_or_404(Specialty, code=self.kwargs['vacancy_type'])
        return Vacancy.objects.filter(specialty=specialty)


class CompanyView(View):
    model = Company

    def get(self, request, company_id, *args, **kwargs):
        try:
            company = Company.objects.get(pk=company_id)
        except ObjectDoesNotExist:
            raise Http404("Компании с таким id не существует")
        vacancies_by_company = Vacancy.objects.filter(company=company.id)
        context = {
            'company': company,
            'vacancies': vacancies_by_company
        }
        return render(request, 'vacancies/company.html', context=context)


class VacancyView(View):
    model = Vacancy
    template_name = 'vacancies/vacancy.html'

    def get(self, request, vacancy_id, *args, **kwargs):
        try:
            vacancy = Vacancy.objects.get(pk=vacancy_id)
        except ObjectDoesNotExist:
            raise Http404("Вакансии с таким id не существует")
        context = {
            'vacancy': vacancy,
            'form': SendApplicationForm
        }
        return render(request, 'vacancies/vacancy.html', context=context)

    def post(self, request, vacancy_id):
        vacancy = Vacancy.objects.get(pk=vacancy_id)
        if request.method == 'POST':
            send_application_form = SendApplicationForm(request.POST)
            if send_application_form.is_valid():
                application = send_application_form.save(commit=False)
                application.user = request.user
                application.vacancy = vacancy
                application.save()
                return redirect('application_sent', self.kwargs['vacancy_id'])
        else:
            send_application_form = SendApplicationForm()
        return render(request, 'vacancies/vacancy.html', context={'form': send_application_form,
                                                                  'vacancy': vacancy})


class SentView(TemplateView):
    template_name = 'vacancies/sent.html'

    def get_context_data(self, vacancy_id, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancy_id'] = vacancy_id
        return context


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'vacancies/register.html'
    success_url = reverse_lazy('login')


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'vacancies/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


class MyCompanyLetsStartView(TemplateView):
    template_name = 'vacancies/company-create.html'


class MyCompanyCreateView(CreateView):
    form_class = MyCompanyForm
    template_name = 'vacancies/company-edit.html'
    # success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):

        context = {
                'form': MyCompanyForm,
                'isCompanyClick': "nav-link active",
                'isVacancyClick': "nav-link"
                }
        return render(request, 'vacancies/company-edit.html', context=context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            mycompany_form = MyCompanyForm(request.POST, request.FILES)
            if mycompany_form.is_valid():
                mycompany = mycompany_form.save(commit=False)
                mycompany.owner = request.user
                mycompany.save()
                return redirect('home')
        else:
            mycompany_form = MyCompanyForm()
        return render(request, 'vacancies/company-edit.html', context={'form': mycompany_form,
                                                                       'isCompanyClick': "nav-link active",
                                                                       'isVacancyClick': "nav-link",
                                                                       })


class MyCompanyFullView(UpdateView):
    form_class = MyCompanyForm
    template_name = 'vacancies/company-edit.html'
    # success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        try:
            mycompany = Company.objects.get(owner=request.user)
        except ObjectDoesNotExist:
            mycompany = None
        if not mycompany:
            return redirect('letsstart_mycompany')
        else:
            filled_form = MyCompanyForm(instance=mycompany)
            context = {
                'form': filled_form,
                'isCompanyClick': "nav-link active",
                'isVacancyClick': "nav-link"
            }
            return render(request, 'vacancies/company-edit.html', context=context)

    def post(self, request, *args, **kwargs):
        mycompany = Company.objects.get(owner=request.user)
        if request.method == 'POST':
            mycompany_form = MyCompanyForm(request.POST, request.FILES, instance=mycompany)
            if mycompany_form.is_valid():
                mycompany = mycompany_form.save(commit=False)
                mycompany.owner = request.user
                mycompany.save()
                return redirect('mycompany')
        else:
            mycompany_form = MyCompanyForm(instance=mycompany)
        return render(request, 'vacancies/company-edit.html', context={'form': mycompany_form})


class MyCompanyVacanciesView(ListView):
    model = Vacancy
    template_name = 'vacancies/vacancy-list.html'

    def get(self, request, *args, **kwargs):
        vacancies_by_company = None
        try:
            mycompany = Company.objects.get(owner=request.user)
            vacancies_by_company = Vacancy.objects.filter(company=mycompany.pk)
        except ObjectDoesNotExist:
            mycompany = None
        context = {
            'mycompany': mycompany,
            'vacancies': vacancies_by_company,
            'isCompanyClick': "nav-link",
            'isVacancyClick': "nav-link active"
        }
        return render(request, 'vacancies/vacancy-list.html', context=context)


class MyCompanyCreateVacancyView(CreateView):
    form_class = MyVacancyForm
    template_name = 'vacancies/vacancy-edit.html'
    success_url = reverse_lazy('home')

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


class MyCompanyVacancyFullView(UpdateView):
    form_class = MyVacancyForm
    template_name = 'vacancies/vacancy-edit.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        mycompany = Company.objects.get(owner=request.user)
        vacancies_by_company = Vacancy.objects.filter(company=mycompany.pk)
        myvacancy = get_object_or_404(Vacancy, pk=self.kwargs['vacancy_id'])
        applications = Application.objects.filter(vacancy=self.kwargs['vacancy_id'])

        if myvacancy not in vacancies_by_company:
            raise Http404('У вашей компании нет вакансии с таким id')
        else:
            filled_form = MyVacancyForm(instance=myvacancy)
            context = {
                'applications': applications,
                'myvacancy': myvacancy,
                'form': filled_form,
                    }
        return render(request, 'vacancies/vacancy-edit.html', context=context)

    def post(self, request, **kwargs):
        myvacancy = Vacancy.objects.get(pk=self.kwargs['vacancy_id'])
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
    return HttpResponseNotFound(exception)


def custom_handler500(request):
    return HttpResponseServerError("Ошибка сервера!")
