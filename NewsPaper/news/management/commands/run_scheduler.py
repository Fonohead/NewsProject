import logging
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

logger = logging.getLogger(__name__)


# Функция запуска рассылки дайджеста
def weekly_digest_job():
    logger.info("Запуск еженедельной рассылки дайджеста...")
    call_command('send_weekly_digest')


# Очистка старых логов выполнения задач из БД
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Запуск планировщика задач APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)

        # Настраиваем хранилище задач прямо в базе данных Django
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Регистрируем задачу рассылки дайджеста
        scheduler.add_job(
            weekly_digest_job,
            trigger=CronTrigger(day_of_week="sun", hour=20, minute=00),
            id="weekly_digest",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Задача 'weekly_digest' успешно зарегистрирована.")

        # Регистрируем задачу очистки логов (каждый понедельник в полночь)
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week='mon', hour=00, minute=00),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )

        try:
            logger.info("Запуск планировщика...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Остановка планировщика...")
            scheduler.shutdown()
            logger.info("Планировщик успешно остановлен.")
