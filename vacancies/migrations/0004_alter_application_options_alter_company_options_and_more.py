# Generated by Django 4.0.2 on 2022-03-08 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0003_alter_application_options_alter_company_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application',
            options={'verbose_name': 'Отклик', 'verbose_name_plural': 'Отклики'},
        ),
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': 'Компания', 'verbose_name_plural': 'Компании'},
        ),
        migrations.AlterModelOptions(
            name='specialty',
            options={'verbose_name': 'Специализация', 'verbose_name_plural': 'Специализации'},
        ),
        migrations.AlterModelOptions(
            name='vacancy',
            options={'verbose_name': 'Вакансия', 'verbose_name_plural': 'Вакансии'},
        ),
    ]
