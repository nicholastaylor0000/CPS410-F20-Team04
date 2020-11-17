from django import forms

class SearchDatesForm(forms.Form):
    search = forms.CharField(required=False)
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)


class SearchClaimedForm(forms.Form):
    filter = forms.ChoiceField(
        choices = (
            ('all', 'All Events'), 
            ('claimed', 'Reserved Slots'), 
            ('unclaimed', 'Unreserved Slots')),
        required=False,
    )