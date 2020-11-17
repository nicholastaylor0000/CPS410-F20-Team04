from django.apps import AppConfig

class ScheduleConfig(AppConfig):
    name = 'schedule'
    verbose_name = 'django-scheduler'

class SchedulerConfig(AppConfig):
    name = 'scheduler'
    verbose_name = 'Scheduler and Calendar App'