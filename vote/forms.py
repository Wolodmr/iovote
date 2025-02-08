from django import forms
from voting_sessions.models import Option
from vote.models import Vote

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['option']

    def __init__(self, *args, **kwargs):
        session = kwargs.pop('session', None)
        super().__init__(*args, **kwargs)
        if session:
            self.fields['option'].queryset = Option.objects.filter(session=session)

    def clean(self):
        cleaned_data = super().clean()
        user = self.initial.get('user')
        option = cleaned_data.get('option')

        if user and option and Vote.objects.filter(user=user, option__session=option.session).exists():
            raise forms.ValidationError("You have already voted in this session.")
        return cleaned_data

