# voting_sessions/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Session, Option  
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

def session_list(request):
    sessions = Session.objects.all()
    return render(request, "session_list.html", {"sessions": sessions})

@login_required
def session_detail(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    return render(request, "session_detail.html", {"session": session})


@login_required  
def vote(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    from vote.models import Vote
    if request.method == 'POST':
        option_id = request.POST.get('option')
        option = get_object_or_404(Option, id=option_id, session=session)
        try:
            # Check if the user has already voted in this session
            if Vote.objects.filter(user=request.user, option__session=session).exists():
                messages.error(request, "You have already voted in this session.")
            else:
                # Create a new vote
                Vote.objects.create(user=request.user, option=option)
                messages.success(request, "Your vote has been cast successfully!")
            return redirect('voting_sessions:session_detail', session_id=session_id)
        except ValidationError as e:
            messages.error(request, str(e))
    else:
        options = session.options.all()
        return render(request, 'vote/vote.html', {'session': session, 'options': options})




