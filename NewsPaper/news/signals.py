from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import PostCategory, CategorySubscribers

from NewsPaper.settings import DEFAULT_FROM_EMAIL


@receiver(m2m_changed, sender=PostCategory)
def notify_post_create(sender, instance, action, **kwargs):
    if action == 'post_add':
        for cat in instance.Category.all():
            for subscribe in CategorySubscribers.objects.filter(categoryThrough=cat):

                msg = EmailMultiAlternatives(
                    subject=instance.title,
                    body=instance.text,
                    from_email=DEFAULT_FROM_EMAIL,
                    to=[subscribe.subscriberThrough.email],
                )

                html_content = render_to_string(
                    'post_create.html',
                    {
                        'post': instance.text,
                        'recipient': subscribe.subscriberThrough.email,
                        'category_name': subscribe.categoryThrough,
                        'subscriber_user': subscribe.subscriberThrough,
                        'pk_id': instance.pk,
                    },
                )

                msg.attach_alternative(html_content, "text/html")
                msg.send()


