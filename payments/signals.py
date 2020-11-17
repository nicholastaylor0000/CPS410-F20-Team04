from django.shortcuts import get_object_or_404
from paypal.standard.ipn.signals import valid_ipn_received
from scheduler.models import ScheduleEvent
from django.dispatch import receiver

@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == 'Completed':
        def is_confirmed(self):
            ScheduleEvent.is_claimed = True