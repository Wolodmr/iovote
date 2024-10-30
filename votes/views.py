from .models import Vote, Participation, VotingSession, VotingOption, Reader, PreliminaryVoting
from django.shortcuts import render, get_object_or_404, redirect
from .forms import VotingForm, VotingSessionForm
from django.db.models import Count
from .utils import send_voting_invitation
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('index')  # Redirect to the home page or wherever you prefer
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def index(request):
    # Fetch all available voting sessions
    sessions = VotingSession.objects.all()

    # Render only the sessions on the 'Home' page
    return render(request, 'votes/index.html', {'sessions': sessions})

def vote_for_mode_view(request, session_id):
    session = VotingSession.objects.get(id=session_id)

    if request.method == 'POST':
        if 'open' in request.POST:
            session.open_votes_count += 1
        session.save()
        return redirect('results', session_id=session.id)

    return render(request, 'vote_for_mode.html', {'session': session})
    

def results(request, session_id):
    # Get the voting session
    session = get_object_or_404(VotingSession, id=session_id)
    
    # Get all the votes for this session
    votes = Vote.objects.filter(session=session)
    
    # Determine if the voting is open or closed
    if session.voting_preference == 'open':
        # Open voting - display voter names with votes
        context = {
            'session': session,
            'votes': votes,
            'show_voters': True,  # Set a flag to show voter names
        }
    else:
        # Closed voting - hide voter names
        context = {
            'session': session,
            'votes': votes,
            'show_voters': False,  # Set a flag to hide voter names
        }

    options = VotingOption.objects.all()
    votes = Vote.objects.all()
    vote_count = {option: votes.filter(option=option).count() for option in options}
    return render(request, 'votes/results.html', context)

from .models import PreliminaryVoting, VotingSession

def results_view(request, session_id):
    session = get_object_or_404(VotingSession, id=session_id)
    
    # Count open and closed votes
    open_votes_count = PreliminaryVoting.objects.filter(session=session, preference="open").count()
    closed_votes_count = PreliminaryVoting.objects.filter(session=session, preference="closed").count()
    total_votes = open_votes_count + closed_votes_count
    
    # Calculate percentages
    open_percentage = (open_votes_count / total_votes * 100) if total_votes > 0 else 0
    closed_percentage = (closed_votes_count / total_votes * 100) if total_votes > 0 else 0

    context = {
        'session': session,
        'open_votes_count': open_votes_count,
        'closed_votes_count': closed_votes_count,
        'open_percentage': open_percentage,
        'closed_percentage': closed_percentage,
    }
    return render(request, 'votes/results.html', context)
# import logging

# logger = logging.getLogger(__name__)

# from django.shortcuts import get_object_or_404, redirect, render
# from .models import VotingSession, VotingOption, Vote

# def vote(request, session_id):
#     session = get_object_or_404(VotingSession, pk=session_id)
    
#     if request.method == 'POST':
#         option_id = request.POST.get('option')

#         logger.debug(f"[DEBUG] Session ID: {session_id}, Voting Preference: {session.voting_preference}, Option ID: {option_id}")

#         if option_id:
#             # Check if the voting preference is for preliminary voting
#             if session.voting_preference == 'preliminary':
#                 existing_vote = PreliminaryVoting.objects.filter(session=session, user=request.user).exists()
#                 logger.debug(f"[DEBUG] Preliminary vote exists: {existing_vote}")

#                 if not existing_vote:
#                     # Create a new preliminary vote
#                     PreliminaryVoting.objects.create(session=session, user=request.user, preference=option_id)
#                     logger.debug("[DEBUG] Preliminary vote recorded successfully")
#                 else:
#                     logger.debug("[DEBUG] User has already voted in preliminary voting.")
#             else:
#                 # Logic for main voting
#                 option = get_object_or_404(VotingOption, pk=option_id)
#                 if not Vote.objects.filter(user=request.user, session=session).exists():
#                     Vote.objects.create(user=request.user, session=session, option=option)
#                     option.votes += 1
#                     option.save()
#                     logger.debug("[DEBUG] Main vote recorded successfully")

#         return redirect('results', session_id=session_id)

#     return render(request, 'votes/vote.html', {'session': session, 'options': session.votingoption_set.all()})




# views.py
from django.shortcuts import render, redirect
from .models import VotingSession, VotingOption
import logging

logger = logging.getLogger(__name__)

def create_voting_session(request):
    if request.method == 'POST':
        # Create a new VotingSession instance
        session = VotingSession.objects.create(
            is_active=True,  # Set the session as active
            is_started=True,  # Set the session as not started
            start_date=timezone.now(),  # Set the current time as the start date
            # Set other required fields here if necessary
        )
        VotingOption.objects.create(session=session, name="Open")
        VotingOption.objects.create(session=session, name="Closed")
        
        return redirect('index')  # Replace with the name of the view you want to redirect to

    return render(request, 'votes/create_voting_session.html')


def preliminary_voting_active(session):
    current_time = timezone.now()
    end_of_preliminary_voting = session.preliminary_voting_ends()
    return current_time <= end_of_preliminary_voting

from django.shortcuts import render
from .models import VotingSession, VotingOption, Vote
from django.utils import timezone

def general_results_view(request):
 
    try:
        current_session = VotingSession.objects.filter(start_date__lte=timezone.now()).latest('start_date')
        preliminary_votes = current_session.preliminary_votes_count()

        print(f"[DEBUG] Current session: {current_session}")  # Debugging output
        print(f"[DEBUG] Preliminary votes passed to template: {preliminary_votes}")  # Debugging output

        context = {
            'session': current_session,
            'preliminary_votes': preliminary_votes,
        }
    except VotingSession.DoesNotExist:
        print("[DEBUG] No active voting session found.")  # Debugging output
        context = {
            'session': None,
            'preliminary_votes': 0,
        }


    return render(request, 'votes/results.html', context)


def start_voting_session(request, session_id):
    session = get_object_or_404(VotingSession, id=session_id)
    
    # Check if the session has already started
    if session.is_started:
        # Redirect to the results page or show a message
        return redirect('results', session_id=session.id)  # Session already started
    
    # Set the current time as start_time and mark the session as started
    session.start_time = timezone.now()
    session.is_started = True  # Mark the session as started
    session.save()

    # Send the initial invitation
    send_voting_invitation(session, invitation_type='initial')
    
    return redirect('results', session_id=session.id)  # Redirect to the results page after starting


def send_reminder(request, session_id):
    session = VotingSession.objects.get(id=session_id)
    # Logic to check if it's 10 days before the main vote
    send_voting_invitation(session, invitation_type='reminder')  # Reminder invitation


def stop_voting_session(request, session_id):
    session = get_object_or_404(VotingSession, id=session_id)
    
    # Check if the session is active
    if not session.is_active:
        return redirect('results', session_id=session.id)  # Session already stopped

    # Mark the session as inactive and set the end time
    session.is_active = False
    session.end_time = timezone.now()
    session.save()

    # Redirect to the results page
    return redirect('results', session_id=session.id)

from django.shortcuts import get_object_or_404
from django.contrib import messages

def preliminary_vote(request, session_id):
    # Fetch the session object and check if preliminary voting is active
    session = get_object_or_404(VotingSession, id=session_id)
    
    # Check if the user has already voted in this preliminary session
    if Vote.objects.filter(user=request.user, session=session, timestamp__lt=session.preliminary_voting_ends()).exists():
        messages.info(request, "You have already cast your preliminary vote.")
        return redirect('index')
    
    # Process the form submission
    if request.method == 'POST':
        vote_option = request.POST.get('vote_option')  # Options: "open" or "closed"
        
        # Ensure a valid option was selected
        if vote_option in ["open", "closed"]:
            if vote_option == "open":
                session.open_votes_count += 1
            else:
                session.closed_votes_count += 1
            session.save()
            
            # Record the vote in the Vote model for historical purposes
            Vote.objects.create(user=request.user, session=session, option=None, no_support=False, timestamp=timezone.now())
            
            messages.success(request, 'Your preliminary vote has been recorded!')
            return redirect('index')
        else:
            messages.error(request, "Invalid voting option selected.")
    
    # If preliminary voting has ended
    if not preliminary_voting_active(session):
        messages.error(request, 'Preliminary voting has ended!')
        return redirect('index')

    return render(request, 'votes/preliminary_vote.html', {'session': session})


from django.shortcuts import render, get_object_or_404
from .models import VotingSession, VotingOption, PreliminaryVoting

from django.shortcuts import render, get_object_or_404
from .models import VotingSession, VotingOption, PreliminaryVoting, Vote

# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import VotingSession, VotingOption, PreliminaryVoting, Vote
from .forms import VotingForm
from django.contrib.auth.decorators import login_required

@login_required
def vote_view(request, session_id):
    session = get_object_or_404(VotingSession, id=session_id)
    options = VotingOption.objects.filter(session=session)

    if request.method == "POST":
        # Debugging: print all POST data
        print("[DEBUG] POST data:", request.POST)

        selected_mode = request.POST.get('voting_mode')
        selected_options = request.POST.getlist('options')

        print("[DEBUG] Selected voting mode:", selected_mode)
        print("[DEBUG] Selected options:", selected_options)

        if selected_mode in ["open", "closed"]:
            PreliminaryVoting.objects.create(
                session=session,
                user=request.user,
                preference=selected_mode
            )
            print(f"[DEBUG] Recorded preliminary vote for: {selected_mode} in PreliminaryVoting table")
        elif selected_options:
            for option_id in selected_options:
                try:
                    selected_vote_option = VotingOption.objects.get(id=option_id, session=session)
                    Vote.objects.create(
                        user=request.user,
                        option=selected_vote_option,
                        session=session
                    )
                    print(f"[DEBUG] Recorded main vote for: {selected_vote_option.name} in Vote table")
                except VotingOption.DoesNotExist:
                    print(f"[DEBUG] Voting option with ID '{option_id}' does not exist.")

        return redirect('results', session_id=session.id)

    return render(request, 'votes/vote.html', {'options': options, 'session': session})






def cast_vote_view(request, session_id):
    session = VotingSession.objects.get(id=session_id)
    if request.method == 'POST':
        option_id = request.POST.get('option')  # Get the selected option ID
        option = VotingOption.objects.get(id=option_id)
        
        # Create a new vote
        Vote.objects.create(user=request.user, option=option, session=session)
        
        return redirect('results')  # Redirect to results page after voting




