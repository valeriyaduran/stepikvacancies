"""stepik_vacancies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from vacancies.views import MainView, VacanciesView, VacancyTypeView, CompanyView, VacancyView, custom_handler404, \
    custom_handler500, SentView, UserRegisterView, UserLoginView, UserLogoutView, \
    MyCompanyCreateView, MyCompanyFullView, MyCompanyVacanciesView, \
    MyCompanyLetsStartView, MyCompanyVacancyFullView, MyCompanyCreateVacancyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='home'),
    path('vacancies/', VacanciesView.as_view(), name='vacancies'),
    path('vacancies/cat/<slug:vacancy_type>/', VacancyTypeView.as_view(), name='vacancy_type'),
    path('companies/<int:company_id>/', CompanyView.as_view(), name='company'),
    path('vacancies/<int:vacancy_id>/', VacancyView.as_view(), name='vacancy'),
    path('vacancies/<int:vacancy_id>/send/', SentView.as_view(), name='application_sent'),
    path('mycompany/letsstart/', MyCompanyLetsStartView.as_view(), name='letsstart_mycompany'),
    path('mycompany/create/', MyCompanyCreateView.as_view(), name='create_mycompany'),
    path('mycompany/', MyCompanyFullView.as_view(), name='mycompany'),
    path('mycompany/vacancies/', MyCompanyVacanciesView.as_view(), name='mycompany_vacancies'),
    path('mycompany/vacancies/create/', MyCompanyCreateVacancyView.as_view(), name='mycompany_create_vacancy'),
    path('mycompany/vacancies/<int:vacancy_id>/', MyCompanyVacancyFullView.as_view(), name='mycompany_vacancy'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout')
]

handler404 = custom_handler404
handler500 = custom_handler500

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
