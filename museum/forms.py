from django import forms
from .models import Museum, Group
from user.models import UserProfile

class CreateGroupForm(forms.Form):
    name = forms.CharField(max_length=50)
    number = forms.IntegerField(min_value=1, max_value=200)
    museum = forms.ModelChoiceField(Museum.objects.all())

    def create_users_pdf(self, user):
        museum = self.cleaned_data['museum']
        name = self.cleaned_data['name']

        group = Group(
            museum=museum, 
            name=name, 
            created_by=user
        )
        group.save()
        tokens = []
        for x in range(self.cleaned_data['number']):
            profile = UserProfile()
            profile.display_name = f'space cadet {x + 1}'
            profile.save()
            group.profiles.add(profile)
            museum.profiles.add(profile)
            tokens.append(profile.qr_token)

        group.save()
        museum.save()