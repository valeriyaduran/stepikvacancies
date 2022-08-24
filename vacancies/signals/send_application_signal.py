import django.dispatch
from django.db.models.signals import post_save
from django.dispatch import receiver

from vacancies.models import Application

application_signal = django.dispatch.Signal()


@receiver(post_save, sender=Application)
def send_application(**kwargs):
    print(f"Письмо отправлено на почту {kwargs['instance'].written_email}")
