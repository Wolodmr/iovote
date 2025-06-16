import os
import django

# ✅ Set up Django before accessing models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iovote.settings")
django.setup()

from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
from django.apps import apps

# ✅ Create Dash app using Flask server
app = Dash(__name__)

def get_results_data():
    try:
        apps.check_models_ready()  # Ensure Django models are ready
        Result = apps.get_model('results', 'Result')  # Get the Result model
        results = Result.objects.all()  # Fetch results from DB
        return [{"option": result.option, "votes": result.votes} for result in results]
    except Exception as e:
        print(f"⚠️ Error loading data: {e}")
        return []

def update_dashboard():
    try:
        data = get_results_data()
        df = pd.DataFrame(data) if data else pd.DataFrame({"option": ["No Data"], "votes": [0]})

        fig = px.bar(df, x="option", y="votes", title="Vote Results")

        app.layout = html.Div([
            html.H3("Vote Results Dashboard"),
            dcc.Graph(figure=fig)
        ])

    except Exception as e:
        print(f"⚠️ Error creating dashboard: {e}")

update_dashboard()

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)  # Run Dash on port 8050
