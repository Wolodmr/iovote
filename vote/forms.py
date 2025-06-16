# vote/forms.py
from django import forms
from .models import Vote
from voting_sessions.models import Option


class VoteForm(forms.ModelForm):
    """
    Form for casting a vote.

    Attributes:
        option (ModelChoiceField): Field for selecting an option, displayed as radio buttons.
    """
    option = forms.ModelChoiceField(queryset=Option.objects.none(), widget=forms.RadioSelect)

    class Meta:
        model = Vote
        fields = ['option']

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with a specific session and user.

        Args:
            session (Session): The voting session associated with the form.
            user (User): The user submitting the vote.
        """
        session = kwargs.pop('session')
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['option'].queryset = session.options.all()
        self.instance.session = session
        self.instance.user = user


