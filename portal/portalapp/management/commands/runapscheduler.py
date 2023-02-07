import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from portalapp.models import Article
from django.contrib.auth.models import User

from datetime import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from portal.settings import DEFAULT_FROM_EMAIL




logger = logging.getLogger(__name__)


# еженедельная рассылка
def my_job():
    news_list = []
    week = datetime.now().isocalendar()[1] - 2

    for article in Article.objects.all().values('id', 'title',):
        info = ({article.get("id")}, {article.get("title")})
        news_list.append(info)

    users = User.objects.all()

    for user in users:
        html_content = render_to_string(
            'article_scheduler.html', {'user': user,
                                       'news': news_list,
                                       'week': week})

        msg = EmailMultiAlternatives(
            subject=f'Привет, {user.username}! Направляем новые объявления за неделю',
            from_email=DEFAULT_FROM_EMAIL,
            to=[user.email]
        )

        if news_list:
            msg.attach_alternative(html_content, 'text/html')
            msg.send()


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