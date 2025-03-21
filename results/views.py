# results/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from voting_sessions.models import Session
from vote.models import Vote
from django.shortcuts import render
from django_plotly_dash.templatetags import plotly_dash
from django_plotly_dash import DjangoDash
from django_plotly_dash.templatetags.plotly_dash import plotly_app
from dash import dcc, html
import plotly.express as px
import pandas as pd
from django.apps import apps

# ✅ Initialize Dash App inside views.py
def initialize_dash():
    print("✅ Initializing Dash App after Django models are ready.")
    return DjangoDash("votes_result")

app = None  # Placeholder for Dash instance


def get_results_data():
    """Fetch results data dynamically after ensuring models are ready."""
    try:
        apps.check_models_ready()
        Result = apps.get_model('results', 'Result')
        results = Result.objects.all()
        return [{"option": result.option, "votes": result.votes} for result in results]
    except Exception as e:
        print(f"⚠️ Error loading data: {e}")
        return []

def create_dashboard():
    """Create the dashboard layout and fetch data dynamically."""
    try:
        apps.check_models_ready()
        Result = apps.get_model('results', 'Result')

        if not Result.objects.exists():
            print("⚠️ No data in the database.")
            df = pd.DataFrame({"option": ["No Data"], "votes": [0]})
        else:
            print("✅ Data successfully loaded!")
            data = get_results_data()
            df = pd.DataFrame(data)

        fig = px.bar(df, x="option", y="votes", title="Vote Results")

        # ✅ Update layout dynamically
        app.layout = html.Div([
            dcc.Graph(id="vote-graph", figure=fig)
        ])
    
    except Exception as e:
        print(f"⚠️ Error creating dashboard: {e}")

# ✅ Ensure dashboard is initialized
def load_dashboard(sender, **kwargs):
    global app
    if app is None:  # Initialize Dash only once
        app = initialize_dash()
    create_dashboard()

from django.db.models.signals import post_migrate
post_migrate.connect(load_dashboard)

# ✅ Django View
def results_dashboard(request):
    return render(request, "results_dashboard.html")

def dashboard_view(request):
    return render(request, "results/dashboard.html")

def results_dashboard(request):
    """Render the results page with Dash app"""
    return render(request, "results/results_dashboard.html")

def results_detail(request, session_id):
    """
    Display the detailed results of a voting session with total votes and percentages.
    """
    session = get_object_or_404(Session, id=session_id)
    
    # Retrieve votes associated with the session
    votes = Vote.objects.filter(option__session=session)
    
    # Aggregate vote counts per option
    vote_counts = votes.values('option__title').annotate(count=Count('id'))
    
    # Compute total votes
    total_votes = sum(vote["count"] for vote in vote_counts)

    # Calculate percentage for each option
    for vote in vote_counts:
        vote["percentage"] = (vote["count"] / total_votes * 100) if total_votes > 0 else 0

    return render(request, 'results/results_detail.html', {
        'session': session,
        'vote_counts': vote_counts,
        'total_votes': total_votes,
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
