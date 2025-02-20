# vote/forms.py
from django import forms
from .models import Vote
from voting_sessions.models import Option

class VoteForm(forms.ModelForm):
    option = forms.ModelChoiceField(queryset=Option.objects.none(), widget=forms.RadioSelect)

    class Meta:
        model = Vote
        fields = ['option']

    def __init__(self, *args, **kwargs):
        session = kwargs.pop('session')
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['option'].queryset = session.options.all()
        self.instance.session = session
        self.instance.user = user

