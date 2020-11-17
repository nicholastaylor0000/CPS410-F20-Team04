from django.db import models
from user.models import UserProfile
from museum.models import Simulator, Museum
from schedule.models import Event

# Create your models here.
'''
@DeprecationWarning
class GameEvent(Event):
    game_event_id = models.AutoField(primary_key=True,default=None)
    pilot = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, name="pilot", null=True, blank=True, related_name="pilot_event",
    )
    copilot = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, name="copilot", null=True, blank=True, related_name="copilot_event",
    )
    simulator = models.ForeignKey(Simulator, on_delete=models.CASCADE)
    is_claimed = models.BooleanField(verbose_name="Event is claimed and confirmed", name="is_claimed", default=False)

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.simulator.__str__ + " " + self.start

    def event_duration(self):
        return self.end - self.start

    def is_confirmed(self):
        #TODO Add logic to check confirmation of payment
        return True
'''

class ScheduleEvent(Event):
    pilot = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, name="pilot", null=True, blank=True, related_name="pilot_event",
    )
    copilot = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, name="copilot", null=True, blank=True, related_name="copilot_event",
    )
    simulator = models.ForeignKey(Simulator, on_delete=models.CASCADE)
    is_claimed = models.BooleanField(verbose_name="Event is claimed and confirmed", name="is_claimed", default=False)

    def is_confirmed(self):
        #TODO Add logic to check confirmation of payment
        return True