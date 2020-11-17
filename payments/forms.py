from django import forms

class PaymentsForm(forms.Form):
    card = forms.CharField(required=False)
    
    )