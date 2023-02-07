from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Response
from portal.settings import DEFAULT_FROM_EMAIL

@receiver(post_save, sender=Response)
def response_notifications(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject='Информация от портала: Новый отклик',
            message=f'На ваше объявление "{instance.article.title}" пришёл отклик от пользователя {instance.author.username}: {instance.text}',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[f'{instance.article.author.email}']
        )
    else:
        send_mail(
            subject='Информация от портала: Отклик принят!',
            message=f'Ваш отклик на объявление "{instance.article.title}" был принят пользователем {instance.article.author}.',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[f'{instance.author.email}']
        )