from django.contrib import admin
from .models import Company, Specialty, Vacancy, Application


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'logo', 'description', 'employee_count', 'owner')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'location', 'owner')
    ordering = ['id']


class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'title', 'picture')
    list_display_links = ('id', 'code', 'title')
    search_fields = ('code', 'title')
    ordering = ['id']


class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'skills', 'salary_min', 'salary_max', 'published_at')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    ordering = ['id']


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'written_username', 'written_phone')
    list_display_links = ('id', 'written_username')
    search_fields = ('written_username',)
    ordering = ['id']


admin.site.register(Company, CompanyAdmin)
admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Application, ApplicationAdmin)
