# utils.py (or place it in your views.py)

from django.core.mail import send_mail
from django.conf import settings
from .models import Reader

def send_voting_invitation(session):
    subject = 'Invitation to Vote in the Library Voting Session'
    message = f'You are invited to vote in the upcoming library voting session: {session.title}.\n\nVisit the site to cast your vote!'
    
    # Collect emails from registered readers
    recipient_list = Reader.objects.values_list('email', flat=True)
    
    # Send the email to all readers
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,  # Sender email
        recipient_list,  # Recipient emails
        fail_silently=False,
    )
