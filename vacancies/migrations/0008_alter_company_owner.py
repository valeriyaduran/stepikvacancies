# Generated by Django 4.0.2 on 2022-05-10 09:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vacancies', '0007_alter_vacancy_description_alter_vacancy_salary_max_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='owner',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='companies',
                                       to=settings.AUTH_USER_MODEL),
        ),
    ]
