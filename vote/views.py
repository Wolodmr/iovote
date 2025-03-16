#Vote/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from vote.forms import VoteForm
from vote.models import Vote
from voting_sessions.models import Session

@login_required
def results_detail(request, session_id):
    """
    Display the results of a voting session.

    Args:
        request: The HTTP request object.
        session_id (int): The ID of the voting session.

    Returns:
        HttpResponse: Renders the results page with vote counts for each option.
    """
    session = get_object_or_404(Session, id=session_id)
    options = session.options.all()
    votes = Vote.objects.filter(option__in=options)
    
    vote_count = votes.count()
    option_votes = {option: votes.filter(option=option).count() for option in options}

    return render(request, 'results/results_detail.html', {
        'session': session,
        'vote_count': vote_count,
        'option_votes': option_votes
    })

@login_required  
def vote(request, session_id):
    """
    Handle voting for a session.

    Ensures that a user can only vote once per session. If the vote is valid, 
    it is saved, and the user is redirected to the results page.

    Args:
        request: The HTTP request object.
        session_id (int): The ID of the voting session.

    Returns:
        HttpResponse: Renders the voting form or redirects upon success/failure.
    """
    session = get_object_or_404(Session, id=session_id)

    # Check if the user has already voted in this session
    if Vote.objects.filter(user=request.user, option__session=session).exists():
        messages.error(request, "You have already voted in this session.")
        return redirect('voting_sessions:session_detail', session_id=session_id)

    options = session.options.all()

    if request.method == 'POST':        
        form = VoteForm(request.POST, session=session, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your vote has been cast successfully!")
            return redirect('results:results_detail', session_id=session_id)
    else:
        form = VoteForm(session=session, user=request.user)

    return render(request, 'vote/vote.html', {'form': form, 'session': session, 'options': options})

