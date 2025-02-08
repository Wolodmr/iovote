# vote/views.py
from django.shortcuts import get_object_or_404, render, redirect
from .forms import VoteForm
from vote.models import Vote
from voting_sessions.models import Session, Option
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.core.exceptions import ValidationError
from vote.tasks import example_task
from django.http import HttpResponse
import logging
logger = logging.getLogger(__name__)

def trigger_task(request):
    example_task.delay()  # Trigger the Celery task asynchronously
    return HttpResponse("Task triggered successfully.")

print("NULL")

def submit_vote(request, session_id):
    print('ONE')
    print(f"Session ID: {session_id}")
    print(f"Option ID: {option_id}")
    print(f"User: {request.user}")
    logger.info(f"Request method: {request.method}")
    if request.method == "POST":
        logger.info(f"POST data: {request.POST}")
    if request.method == "POST":
        # Fetch the session
        session = get_object_or_404(Session, id=session_id)

        # Get the selected option
        option_id = request.POST.get("option")
        if not option_id:
            messages.error(request, "You must select an option before submitting.")
            return redirect('vote:vote', session_id=session_id)

        # Fetch the option and ensure it's linked to the correct session
        option = get_object_or_404(session.options, id=option_id)

        # Create the vote
        try:
            Vote.objects.create(user=request.user, option=option)
            messages.success(request, "Your vote has been submitted successfully.")
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('vote:vote', session_id=session_id)

        # Redirect to the results page
        return redirect('vote:result', session_id=session_id)


def vote(request, session_id):
    try:
        session = Session.objects.get(id=session_id)
    except Session.DoesNotExist:
        # Handle the case where the session doesn't exist
        return render(request, 'vote/session_not_found.html')  # Redirect or show a 404 page

    if request.method == 'POST':
        form = VoteForm(request.POST, session=session)
        if form.is_valid():
            vote = form.save(commit=False)
            vote.user = request.user
            vote.session = session
            vote.save()
            messages.success(request, "Your vote has been cast successfully!")
            return redirect('voting_sessions:session_detail', session_id=session_id)
        else:
            messages.error(request, "There was an error with your submission. Please try again.")
    else:
        form = VoteForm(session=session)

    return render(request, 'vote/vote.html', {'form': form, 'session': session})

def result(request):
    render(request, 'vote/result.html')

