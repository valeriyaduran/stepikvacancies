from django.http import Http404, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, TemplateView

from vacancies.models import Specialty, Vacancy, Company


class MainView(TemplateView):
    template_name = 'vacancies/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.all()
        context['companies'] = Company.objects.all()
        return context


class VacanciesView(ListView):
    model = Vacancy
    template_name = 'vacancies/vacancies.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancies'] = Vacancy.objects.all()
        context['specialties'] = Specialty.objects.all()
        return context


class VacancyTypeView(View):
    model = Vacancy
    template_name = 'vacancies/vacancy-type.html'

    def get(self, request, vacancy_type, *args, **kwargs):
        specialty = Specialty.objects.filter(code=vacancy_type)
        if len(specialty) == 0:
            raise Http404("Специализации с таким кодом не существует")
        vacancies_by_specialty = Vacancy.objects.filter(specialty=specialty[0].pk)
        context = {
            'vacancies_by_specialty': vacancies_by_specialty,
        }
        print(vacancies_by_specialty)
        return render(request, 'vacancies/vacancy-type.html', context=context)


class CompanyView(View):
    model = Company
    template_name = 'vacancies/company.html'

    def get(self, request, company_id, *args, **kwargs):
        company = Company.objects.filter(pk=company_id)
        if len(company) == 0:
            raise Http404("Компании с таким id не существует")
        vacancies_by_company = Vacancy.objects.filter(company=company[0].id)
        context = {
            'company': company,
            'vacancies': vacancies_by_company,
        }
        return render(request, 'vacancies/company.html', context=context)


class VacancyView(View):
    model = Vacancy
    template_name = 'vacancies/vacancy.html'

    def get(self, request, vacancy_id, *args, **kwargs):
        vacancy = Vacancy.objects.filter(pk=vacancy_id)
        if len(vacancy) == 0:
            raise Http404("Вакансии с таким id не существует")
        context = {
            'vacancy': vacancy,
        }
        return render(request, 'vacancies/vacancy.html', context=context)


def custom_handler404(request, exception):
    return HttpResponseNotFound(exception)


def custom_handler500(request):
    return HttpResponseServerError("Ошибка сервера!")
