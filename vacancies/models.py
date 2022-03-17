from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from phonenumber_field.modelfields import PhoneNumberField


class Company(models.Model):
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=64)
    logo = models.ImageField(upload_to='MEDIA_COMPANY_IMAGE_DIR')
    description = models.TextField(blank=True)
    employee_count = models.IntegerField()
    owner = models.OneToOneField(User, on_delete=models.PROTECT, related_name='companies', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('company', kwargs={'company_id': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Specialty(models.Model):
    code = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    picture = models.ImageField(upload_to='MEDIA_SPECIALITY_IMAGE_DIR')

    def get_absolute_url(self):
        return reverse('vacancy_type', kwargs={'vacancy_type': self.code})

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    title = models.CharField(max_length=64)
    specialty = models.ForeignKey(Specialty, on_delete=models.PROTECT, related_name="vacancies")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancies")
    skills = models.TextField(blank=True)
    description = models.TextField(blank=True)
    salary_min = models.IntegerField(blank=True)
    salary_max = models.IntegerField(blank=True)
    published_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('vacancy', kwargs={'vacancy_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'


class Application(models.Model):
    written_username = models.CharField(max_length=64, verbose_name='Вас зовут')
    written_phone = PhoneNumberField(null=False, blank=False, verbose_name='Ваш телефон')
    written_cover_letter = models.TextField(blank=True, verbose_name='Сопроводительное письмо')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')

    def __str__(self):
        return self.written_username

    def get_absolute_url(self):
        return reverse('application', kwargs={'vacancy_id': self.pk})

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
