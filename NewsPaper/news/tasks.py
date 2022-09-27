from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from NewsPaper.settings import DEFAULT_FROM_EMAIL
from datetime import timedelta
from django.utils import timezone
from news.models import Category, Post, CategorySubscribers, PostCategory, Author

@shared_task
def my_mail():
    for category in Category.objects.all():

        mailing_list = list(
            CategorySubscribers.objects.filter(
                categoryThrough=category
            ).values_list(
                'subscriberThrough__username',
                'subscriberThrough__first_name',
                'subscriberThrough__email',
                'categoryThrough__categoryName'
            )
        )

        posts_list = list(
            category.posts.filter(
                date__gt= timezone.now().date() - timedelta(days=7)
            ).values_list('id', 'title'))

        if any(
                (all((len(mailing_list) == 1, mailing_list[0][2])),
                 len(mailing_list) > 1)) and len(posts_list) > 0:

            print(mailing_list)
            print(posts_list)

            for user, first_name, email, category_name in mailing_list:
                if not first_name:
                    first_name = user

                html_content = render_to_string(
                    'post_scheduler.html',
                    {
                        'name': first_name,
                        'category': category,
                        'posts': posts_list,
                    }
                )

                message = EmailMultiAlternatives(
                    subject=f'All news in the last week in category"{category}"',
                    from_email=DEFAULT_FROM_EMAIL,
                    to=[email]

                )
                message.attach_alternative(html_content, 'text/html')
                message.send()
