from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from vote.forms import VoteForm
from vote.models import Vote
from voting_sessions.models import Session, Option

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
    # ✅ Optimize by using `prefetch_related` to minimize queries
    session = get_object_or_404(Session.objects.prefetch_related("options"), id=session_id)

    # ✅ Aggregate votes per option in a single query
    option_votes = (
        Option.objects.filter(session=session)
        .annotate(vote_count=Count("votes"))
        .values("id", "title", "vote_count")
    )

    # ✅ Get total vote count efficiently
    vote_count = sum(option["vote_count"] for option in option_votes)

    return render(request, "results/results_detail.html", {
        "session": session,
        "vote_count": vote_count,
        "option_votes": option_votes,
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
    # ✅ Optimize by using `prefetch_related` to fetch related options efficiently
    session = get_object_or_404(Session.objects.prefetch_related("options"), id=session_id)

    # ✅ Optimize vote check by using `.exists()` instead of `.count()`
    if Vote.objects.filter(user=request.user, option__session=session).exists():
        messages.error(request, "You have already voted in this session.")
        return redirect("voting_sessions:session_detail", session_id=session_id)

    options = session.options.all()

    if request.method == "POST":
        form = VoteForm(request.POST, session=session, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your vote has been cast successfully!")
            return redirect("results:results_detail", session_id=session_id)
    else:
        form = VoteForm(session=session, user=request.user)

    return render(request, "vote/vote.html", {"form": form, "session": session, "options": options})
