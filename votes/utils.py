# utils.py (or place it in your views.py)

from django.core.mail import send_mail
from django.conf import settings
from .models import Reader

from django.core.mail import send_mail
from django.conf import settings
from .models import Reader

from django.core.mail import send_mail
from django.conf import settings
from .models import Reader

def send_voting_invitation(session, invitation_type='initial'):
    subject = ''
    message = ''
    
    if invitation_type == 'initial':
        subject = f'Invitation to Vote in the Library Voting Session: {session.name}'
        message = (
            f'You are invited to vote in the upcoming library voting session: {session.name}.\n'
            f'The voting mode is currently set to: {session.voting_preference}.\n'
            'Visit the site to cast your vote!'
        )
    elif invitation_type == 'reminder':
        subject = f'Reminder: Main Voting in the Library Voting Session: {session.name}'
        message = (
            f'This is a reminder to participate in the main vote for the session: {session.name}.\n'
            f'The voting mode is: {session.voting_preference}.\n'
            f'The session will end on: {session.preliminary_voting_ends().strftime("%Y-%m-%d")}.\n'
            'You have until then to cast your vote.'
        )

    recipient_list = list(Reader.objects.values_list('email', flat=True))

    if recipient_list:
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)


