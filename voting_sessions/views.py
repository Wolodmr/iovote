from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.urls import reverse
from .models import Session, Option
from vote.models import Vote

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

    if not session.is_voting_active():
        messages.error(request, "Voting is not allowed because the session has ended.")
        return redirect('voting_sessions:session_list')

    options = {option.id: option for option in session.options.all()}  # Fetch options as a dictionary

    if request.method == 'POST':
        option_id = request.POST.get('option')
        option = options.get(int(option_id))  # Direct dictionary lookup instead of looping

        if not option:
            messages.error(request, "Invalid option selected.")
            return redirect('voting_sessions:session_detail', session_id=session_id)

        # Optimize Vote Check: Use `get()` instead of `filter().exists()`
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
