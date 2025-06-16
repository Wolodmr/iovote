#results/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from voting_sessions.models import Session
from vote.models import Vote
import pandas as pd
from django.apps import apps
from django.db.models.signals import post_migrate
from django.contrib.auth.decorators import login_required


@login_required
def results(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    options = session.options.all()

    # Demo values – Replace with real vote queries later
    demo_votes = {
        "Alice": 30,
        "Bob": 45,
        "Charlie": 25,
    }

    # Total votes
    total_votes = sum(demo_votes.values())

    # Dummy timeline (time vs vote count)
    timeline_data = [
        {"time": "10:00", "votes": 5},
        {"time": "10:15", "votes": 15},
        {"time": "10:30", "votes": 25},
        {"time": "10:45", "votes": 40},
        {"time": "11:00", "votes": 50},
    ]

    # Turnout demo (30 voted, 50 registered)
    registered_users = 50
    voted_users = 30

    context = {
        "session": session,
        "demo_votes": demo_votes,
        "total_votes": total_votes,
        "timeline_data": timeline_data,
        "voted_users": voted_users,
        "registered_users": registered_users,
    }
    return render(request, "results.html", context)


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
