from django.db import models
from django.urls import reverse


class Company(models.Model):
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=64)
    logo = models.URLField(default='https://place-hold.it/100x60')
    description = models.TextField(blank=True)
    employee_count = models.IntegerField()

    def get_absolute_url(self):
        return reverse('company', kwargs={'company_id': self.pk})


class Specialty(models.Model):
    code = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    picture = models.URLField(default='https://place-hold.it/100x60')

    def get_absolute_url(self):
        return reverse('vacancy_type', kwargs={'vacancy_type': self.code})

    def __str__(self):
        return self.code


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
