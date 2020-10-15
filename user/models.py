from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User
import secrets
from django.utils import timezone
from simulator import mail
from utils import render
from simulator.settings import HOST

EXPIRE_AFTER_DAYS = 30

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    qr_token = models.CharField(max_length=24, unique=True)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    date_created = models.DateTimeField(auto_now_add=True)
    is_before_user = models.BooleanField(default=True)
    display_name = models.CharField(max_length=50, blank=True)
    # The name that will show up on the leaderboard
    is_confirmed = models.BooleanField(default=False)   
    ###, email confirmation, like confirming this is your account and intended to login
    confirm_token = models.CharField(max_length=24, unique=True) 
    ## for url address, a unique token for identifying 

    def __str__(self):
        if self.user is None:
            return f'{self.qr_token} Profile'
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):  
        ## save built in function for model, to save any
        if not self.qr_token:
            self.qr_token = secrets.token_hex(12)    
            ### qr token is randomly generated for now, and put in database later
            self.confirm_token = secrets.token_hex(12)

        super().save(*args, **kwargs)

    def is_museum_admin(self):
        if self.user:
            return self.user.museum_set.count() > 0
        else:
            return False
    def is_unused(self):    
        ##Imp: if the user profile has been used to play game or not. Main importance is to delete 
        return self.user is None and self.get_games().count() == 0

    def get_games(self):
        return self.pilot_set.all().union(self.copilot_set.all())

    def total_score(self):
        total = 0
        for gr in self.get_games():
            total += gr.score
        return total

    def total_rides(self):
        return self.get_games().count()

    def total_time(self):
        total = 0
        for gr in self.get_games():
            total += gr.duration()
        return int(total / 60)

    def high_score(self):
        m1 = self.pilot_set.all().aggregate(Max('score'))['score__max']
        m2 = self.copilot_set.all().aggregate(Max('score'))['score__max']
        
        if m1 is None and m2 is None:
            return 'None'
        elif m1 is None:
            return m2
        elif m2 is None:
            return m1
        else:
            return max(m1, m2)

    def get_QR_embedded(self):
        return render.qr_b64(f'{HOST}/register/{self.qr_token}')

    def get_badges(self):
        badges = set()
        for gr in self.get_games():
            for bt in gr.badgetier_set.all():
                badges.add(bt.badge.guid)
        return tuple(badges)
        

def delete_overdue_profiles():   
    ##delete the profile user, if it's never been; For now it's being checked if the profile hasn't been used for at least 30 days
    for profile in UserProfile.objects.all():
        if (profile.user is None
            and (timezone.now() - profile.date_created).days >= EXPIRE_AFTER_DAYS):
            profile.delete()

class PassReset(models.Model): 
     ##Someone tempted to reset the passowrd
    user = models.ForeignKey(User, models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=48, unique=True)
    used =  models.BooleanField(default=False)

    TIMEOUT_SECONDS = 30 * 60    
    ##time constraints to make the password change request successful

    def save(self, *args, **kwargs):  
        ### Sending the email for passowrd reset
        if not self.code:
            self.code = secrets.token_hex(24)    
            ##Creates a code, and the bottom line send it to the random person
            mail.send_pass_email(self.user.email, self.code)
        super().save(*args, **kwargs)

    def is_valid(self):
        return not self.used and (timezone.now() - self.date_created).seconds < self.TIMEOUT_SECONDS

    def __str__(self):
        return self.user.username + ' reset ' + str(self.date_created)