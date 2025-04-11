from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from voting_sessions.models import Session
from vote.models import Vote
from django_plotly_dash import DjangoDash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from django.apps import apps
from django.db.models.signals import post_migrate

# ✅ Initialize Dash App inside views.py (Only once)
app = DjangoDash("votes_result")


def get_results_data():
    """Fetch results data dynamically after ensuring models are ready."""
    try:
        apps.check_models_ready()
        Result = apps.get_model('results', 'Result')

        # ✅ Optimized query to fetch only necessary fields
        results = Result.objects.all().only("option", "votes")

        # ✅ Convert queryset to a list of dictionaries
        return list(results.values("option", "votes"))

    except Exception as e:
        print(f"⚠️ Error loading data: {e}")
        return []



def create_dashboard():
    """Create the dashboard layout and fetch data dynamically."""
    data = get_results_data()

    if not data:
        print("⚠️ No data available.")
        df = pd.DataFrame({"option": ["No Data"], "votes": [0]})
    else:
        print("✅ Data successfully loaded!")
        df = pd.DataFrame(data)

    fig = px.bar(df, x="option", y="votes", title="Vote Results")

    # ✅ Update layout dynamically
    app.layout = html.Div([dcc.Graph(id="vote-graph", figure=fig)])


# ✅ Ensure dashboard is initialized only once
# post_migrate.connect(lambda sender, **kwargs: create_dashboard())
    


# ✅ Django Views
def results_dashboard(request):
    # """Render the results page with Dash app."""
    # return render(request, "results/results_dashboard.html")
    pass


def results_detail(request, session_id):
    """Display the detailed results of a voting session with total votes and percentages."""
    session = get_object_or_404(Session.objects.only("id", "title"), id=session_id)

    # ✅ Aggregate vote counts per option efficiently
    vote_counts = list(
        Vote.objects.filter(option__session=session)
        .values("option__title")
        .annotate(count=Count("id"))
    )

    # ✅ Compute total votes in a single operation
    total_votes = sum(v["count"] for v in vote_counts)

    # ✅ Calculate percentage efficiently
    for v in vote_counts:
        v["percentage"] = (v["count"] / total_votes * 100) if total_votes else 0

    return render(request, "results/results_detail.html", {
        "session": session,
        "vote_counts": vote_counts,
        "total_votes": total_votes,
    })


def results_list(request):
    """Display a list of all voting sessions."""
    sessions = Session.objects.only("id", "title")  # ✅ Fetch only necessary fields
    return render(request, "results/results_list.html", {"sessions": sessions})
