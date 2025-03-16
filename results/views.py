# results/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from voting_sessions.models import Session
from vote.models import Vote

def results_detail(request, session_id):
    """
    Display the detailed results of a voting session.

    Args:
        request: The HTTP request object.
        session_id (int): The ID of the session whose results are displayed.

    Returns:
        HttpResponse: Renders the 'results/results_detail.html' template 
        with session details and vote counts per option.
    """
    session = get_object_or_404(Session, id=session_id)
    # Retrieve votes associated with the session
    votes = Vote.objects.filter(option__session=session)
    # Aggregate vote counts per option
    vote_counts = votes.values('option__title').annotate(count=Count('id'))

    return render(request, 'results/results_detail.html', {
        'session': session,
        'vote_counts': vote_counts,
    })
    
def results_list(request):
    """
    Display a list of all voting sessions.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the 'results/results_list.html' template 
        with a list of all sessions.
    """
    sessions = Session.objects.all()
    return render(request, 'results/results_list.html', {'sessions': sessions})
