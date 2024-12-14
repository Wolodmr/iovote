from django import forms

class VoteForm(forms.Form):
    user = forms.CharField(max_length=100)
    option = forms.CharField(max_length=100)
