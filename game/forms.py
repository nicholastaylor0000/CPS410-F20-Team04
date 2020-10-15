from django import forms

class SearchScoresForm(forms.Form):
    search = forms.CharField(required=False)
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)


class SearchUsersForm(forms.Form):
    search = forms.CharField(required=False)
    filter = forms.ChoiceField(
        choices = (
            ('all', 'all users'), 
            ('reg', 'registered'), 
            ('unreg', 'unregistered')),
        required=False,
    )