from django.db import models
from museum.models import Simulator, Museum
from user.models import UserProfile
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

# A class for respresenting the validated raw data


class GameResult(models.Model):

    pilot = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="pilot_set",
    )
    copilot = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=True, related_name="copilot_set",
    )
    simulator = models.ForeignKey(Simulator, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    score = models.IntegerField()
    num_of_rolls = models.IntegerField()

    def __str__(self):
        if self.copilot:
            return (
                self.pilot.display_name
                + " "
                + self.copilot.display_name
                + " "
                + str(self.start_time)
            )
        else:
            return self.pilot.display_name + str(self.start_time)

    def duration(self):  # checks the time that you were in the simulator
        return (self.end_time - self.start_time).seconds

    def badges(self):
        return self.badgetier_set.all()

    def send_live_result(self):
        if self.copilot:
            copilot = self.copilot.display_name
        else:
            copilot = ''

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "all",
            {
                "type": "receive_result",
                'message': json.dumps({
                    'pilot': self.pilot.display_name,
                    'copilot': copilot,
                    'score': self.score,
                    'badges': tuple(map(
                        lambda badge: badge.icon,
                        self.badges())),
                })
            }
        )
