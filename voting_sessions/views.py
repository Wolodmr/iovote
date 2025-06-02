from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.urls import reverse
from .models import Session, Option
from vote.models import Vote
from django.utils import timezone

def session_invite(request, session_uuid):
    """Handle invitation links and redirect users to the session page."""
    session = get_object_or_404(Session, uuid=session_uuid)

    if not request.user.is_authenticated:
        return redirect(f"{reverse('login')}?next={session.get_invite_link()}")

    return redirect('voting_sessions:session_detail', session_id=session.id)

def session_list(request):
    """Display a list of all voting sessions with preloaded options."""
    sessions = Session.objects.prefetch_related('options')
    return render(request, "session_list.html", {"sessions": sessions})

@login_required
def session_detail(request, session_id):
    """Display details of a specific voting session."""
    session = get_object_or_404(Session.objects.prefetch_related('options'), id=session_id)
    return render(request, "session_detail.html", {"session": session})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.urls import reverse
from .models import Session, Option
from vote.models import Vote
from django.utils import timezone

def session_invite(request, session_uuid):
    """Handle invitation links and redirect users to the session page."""
    session = get_object_or_404(Session, uuid=session_uuid)

    if not request.user.is_authenticated:
        return redirect(f"{reverse('login')}?next={session.get_invite_link()}")

    return redirect('voting_sessions:session_detail', session_id=session.id)

def session_list(request):
    """Display a list of all voting sessions with preloaded options."""
    sessions = Session.objects.prefetch_related('options')
    return render(request, "session_list.html", {"sessions": sessions})

@login_required
def session_detail(request, session_id):
    """Display details of a specific voting session."""
    session = get_object_or_404(Session.objects.prefetch_related('options'), id=session_id)
    return render(request, "session_detail.html", {"session": session})

@login_required
def vote(request, session_id):
    """Allow a user to cast a vote in an active session."""
    session = get_object_or_404(Session.objects.prefetch_related('options'), id=session_id)

    now = timezone.now()
    if now < session.voting_start_time:
        messages.error(request, "Voting is not allowed because the session hasn't started yet.")
        return redirect('voting_sessions:session_detail', session_id=session_id)
    elif now > session.session_end_time:
        messages.error(request, "Voting is not allowed because the session has ended.")
        return redirect('voting_sessions:session_detail', session_id=session_id)

    options = {option.id: option for option in session.options.all()}

    if request.method == 'POST':
        option_id = request.POST.get('option')

        if not option_id:
            messages.error(request, "Please select an option before submitting your vote.")
            return redirect('voting_sessions:session_detail', session_id=session_id)

        try:
            option_id = int(option_id)
            option = options.get(option_id)
        except (ValueError, TypeError):
            messages.error(request, "Invalid option selected.")
            return redirect('voting_sessions:session_detail', session_id=session_id)

        if not option:
            messages.error(request, "Selected option does not exist.")
            return redirect('voting_sessions:session_detail', session_id=session_id)

        existing_vote = Vote.objects.filter(user=request.user, session=session).first()
        if existing_vote:
            messages.error(request, "You have already voted in this session.")
        else:
            try:
                Vote.objects.create(user=request.user, option=option, session=session)
                messages.success(request, "Your vote has been cast successfully!")
            except ValidationError as e:
                messages.error(request, f"Error: {e}")

        return redirect('voting_sessions:session_detail', session_id=session_id)

    return render(request, 'vote/vote.html', {'session': session, 'options': options.values()})

