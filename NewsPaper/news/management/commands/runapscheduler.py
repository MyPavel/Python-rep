import logging

from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news.models import Category, Post, CategorySubscribers, PostCategory, Author

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from NewsPaper.settings import DEFAULT_FROM_EMAIL
from datetime import timedelta
from django.utils import timezone


logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
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


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
