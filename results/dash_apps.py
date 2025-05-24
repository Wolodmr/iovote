# from django_plotly_dash import DjangoDash
# from dash import dcc, html
# import plotly.express as px
# import pandas as pd
# from django.apps import apps

# # ✅ Register the app immediately
# app = DjangoDash("votes_result")

# def get_results_data():
#     try:
#         apps.check_models_ready()
#         Result = apps.get_model('results', 'Result')
#         results = Result.objects.all()
#         return [{"option": result.option, "votes": result.votes} for result in results]
#     except Exception as e:
#         print(f"⚠️ Error loading data: {e}")
#         return []

# def create_dashboard():
#     try:
#         apps.check_models_ready()
#         Result = apps.get_model('results', 'Result')

#         if not Result.objects.exists():
#             print("⚠️ No data found in the database.")
#             df = pd.DataFrame({"option": ["No Data"], "votes": [0]})
#         else:
#             print("✅ Data successfully loaded!")
#             data = get_results_data()
#             df = pd.DataFrame(data)

#         fig = px.bar(df, x="option", y="votes", title="Vote Results")

#         app.layout = html.Div([
#             html.H3("Vote Results Dashboard"),
#             dcc.Graph(figure=fig)
#         ])

#     except Exception as e:
#         print(f"⚠️ Error creating dashboard: {e}")

# # ✅ Ensure it runs after Django models are ready
# from django.db.models.signals import post_migrate
# post_migrate.connect(lambda sender, **kwargs: create_dashboard(), weak=False)
