from .models import Vote, Participation, VotingSession, VotingOption, Reader
from django.shortcuts import render, get_object_or_404, redirect
from .forms import VotingForm, VotingSessionForm
from django.db.models import Count
from .utils import send_voting_invitation
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

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
    

def results(request):
    options = VotingOption.objects.all()
    votes = Vote.objects.all()
    vote_count = {option: votes.filter(option=option).count() for option in options}
    return render(request, 'votes/results.html', {'vote_count': vote_count})


def results_view(request):
    selected_options = VotingOption.objects.filter(selected=True)  # or however you determine selected options
    votes = Vote.objects.filter(option__in=selected_options)  # get votes for those options
    return render(request, 'votes/results.html', {'selected_options': selected_options, 'votes': votes})

def vote(request, session_id):
    # Get the session based on session_id
    session = get_object_or_404(VotingSession, id=session_id)
    
    # Fetch all voting options associated with this session
    options = VotingOption.objects.filter(session=session)
 
    # Handle form submission
    if request.method == 'POST':
        # Get selected options from the form
        selected_options = request.POST.getlist('options')
        no_support = request.POST.get('no_support', False)

        # Ensure the user is logged in
        if request.user.is_authenticated:
            print('auth')
            # Check if the user has already voted in this session to prevent duplicate votes
            if Vote.objects.filter(user=request.user, session=session).exists():
                # Optionally, handle the case where the user has already voted
                return redirect('index')

            # Process the selected options
            if selected_options:
                for option_id in selected_options:
                    # Ensure the option exists and is associated with this session
                    option = get_object_or_404(VotingOption, id=option_id, session=session)
                    # Create a new vote object for each option
                    Vote.objects.create(option=option, session=session, user=request.user)

            # If "no support" is selected, create a vote for "no support"
            if no_support:
                Vote.objects.create(option=None, session=session, user=request.user)

            # Redirect to the results page after voting
            return redirect(reverse('results', args=[session.id]))                        
        
        else:
            # If user is not logged in, you can redirect to login or handle accordingly
            return redirect('login')  # Redirect to the login page if not authenticated
            

    # If the request method is GET (show the voting page)
    return render(request, 'votes/vote.html', {
        'session': session,
        'options': options,
    })




def results_view(request, session_id):
    # Get all votes in the current session
    votes = Vote.objects.filter(session__id=session_id)
    
    # Count the votes for each option
    votes_in_session = votes.filter(no_support=False).values('option__name').annotate(total_votes=Count('option'))
    
    # Count the number of "no support" votes
    no_support_votes = votes.filter(no_support=True).count()

    return render(request, 'votes/results.html', {
        'votes_in_session': votes_in_session,
        'no_support_votes': no_support_votes,
    })


def create_voting_session(request):
    if request.method == 'POST':
        # Assuming you're creating a voting session from a form
        form = VotingSessionForm(request.POST)
        if form.is_valid():
            session = form.save()
            
            # Call the function to send an invitation
            send_voting_invitation(session)
            
            return redirect('some_success_url')
    else:
        form = VotingSessionForm()

    return render(request, 'votes/create_voting_session.html', {'form': form})

def general_results_view(request):
    # Fetch all voting sessions
    sessions = VotingSession.objects.all()

    # Optional: Get a summary of results for each session
    session_results = []
    for session in sessions:
        votes_in_session = Vote.objects.filter(session=session, no_support=False).values('option__name').annotate(total_votes=Count('option'))
        no_support_votes = Vote.objects.filter(session=session, no_support=True).count()

        session_results.append({
            'session': session,
            'votes_in_session': votes_in_session,
            'no_support_votes': no_support_votes
        })

    return render(request, 'votes/general_results.html', {
        'sessions': session_results
    })








