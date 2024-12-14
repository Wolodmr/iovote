from django.shortcuts import render, get_object_or_404, redirect
from .models import Vote
from voting_sessions.models import Session
from .forms import VoteForm

def vote(request, session_id):
    # Get the session object
    session = get_object_or_404(Session, id=session_id)
    
    if request.method == 'POST':
        # Handle form submission
        form = VoteForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            option = form.cleaned_data['option']
            
            # Ensure a user can only vote once per session
            if Vote.objects.filter(session=session, user=user).exists():
                form.add_error(None, "You have already voted in this session.")
                return render(request, 'vote/vote_form.html', {'form': form, 'session': session})
            
            # Save the vote
            Vote.objects.create(session=session, user=user, option=option)
            return redirect('vote/thank_you.html')
    else:
        form = VoteForm()

    return render(request, 'vote/vote_form.html', {'form': form, 'session': session})

def thank_you(request):
    return render(request, 'vote/thank_you.html')


# Create your views here.
