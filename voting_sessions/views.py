import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import os
import io
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.db.models.functions import TruncMinute
from django.db.models import Count
from django.conf import settings
from .models import Session, Option
from vote.models import Vote
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from voting_sessions.models import Session
from .models import SessionAccess

# def charts_redirect_view(request):
#     now = timezone.now()
#     latest_session = Session.objects.filter(
#         session_start_time__isnull=False,
#         session_start_time__lte=now - timezone.timedelta(seconds=Session.choice_duration.default)
#     ).order_by('-session_start_time')

#     if latest_session.exists():
#         return redirect('voting_sessions:session_charts', session_id=latest_session.first().id)
#     else:
#         return redirect('voting_sessions:session_charts')  # Triggers fallback in charts_view
def results(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    
    # Track session access
    if request.user.is_authenticated:
        SessionAccess.objects.update_or_create(
            user=request.user,
            session=session,
            defaults={'accessed_at': timezone.now()}
        )

    context = {"session": session}
    return render(request, "session_charts.html", context)

def charts_redirect_view(request):
    # Only include sessions where voting has started
    eligible_sessions = [
        session for session in Session.objects.all()
        if timezone.now() > session.voting_start_time + timezone.timedelta(seconds=session.choice_duration)
    ]
    # Sort by last_opened (fallback to session_start_time if last_opened is None)
    latest_session = sorted(
        eligible_sessions,
        key=lambda s: s.last_opened,
        reverse=True
    )

    if latest_session:
        return redirect('voting_sessions:session_charts', session_id=latest_session[0].id)
    else:
        return redirect('results:no_charts_available')  # Define this view/template if needed


def charts_view(request, session_id=None):
    if session_id is None:
        return render(request, 'voting_sessions/session_charts.html', {'no_data': True})

    session = get_object_or_404(Session, id=session_id)
    now = timezone.now()

    voting_in_progress = session.session_start_time and (
        session.session_start_time + timezone.timedelta(seconds=session.choice_duration)
    ) > now

    # chart_data = {
    #     'votes_per_option': [...],  # Replace as needed
    #     'vote_percentage': [...],
    #     # More chart data
    # }

    context = {
        'session': session,
        # 'chart_data': chart_data,
        'voting_in_progress': voting_in_progress,
        'current_time': now,
        'no_data': False,
    }
    return render(request, 'voting_sessions/session_charts.html', context)


def generate_base64_chart(fig):
    try:
        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')  # ensures full chart is captured
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        return image_base64
    except Exception as e:
        print("Chart generation error:", e)
        return ""

def session_charts(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    options = Option.objects.filter(session=session)
    votes = [c.votes.count() for c in options]
    names = [c.title for c in options]
    
    # Fix: avoid zero-vote options for percentage chart labels
    filtered_labels = [name if vote > 0 else '' for name, vote in zip(names, votes)]

    # Line chart data
    votes_by_time = (
        Vote.objects.filter(session=session)
        .annotate(minute=TruncMinute('created_at'))
        .values('minute')
        .annotate(vote_count=Count('id'))
        .order_by('minute')
    )
    timestamps = [v['minute'].strftime('%H:%M') for v in votes_by_time]
    counts = [v['vote_count'] for v in votes_by_time]

    # Bar chart
    fig1, ax1 = plt.subplots()
    ax1.bar(names, votes)
    ax1.set_title("Votes per Option")
    chart1 = generate_base64_chart(fig1)

    # Pie chart
    fig2, ax2 = plt.subplots()
    ax2.pie(votes, labels=filtered_labels, autopct=lambda p: f'{p:.1f}%' if p > 0 else '')
    ax2.set_title("Vote Percentages")
    chart2 = generate_base64_chart(fig2)

    # Line chart
    fig3, ax3 = plt.subplots()
    ax3.plot(timestamps, counts, marker='o')
    ax3.set_title("Voting Activity Over Time")
    ax3.set_xlabel("Time")
    ax3.set_ylabel("Votes")
    chart3 = generate_base64_chart(fig3)

    # Turnout chart
    voted_users = Vote.objects.filter(session=session).values('user').distinct().count()
    total_users = User.objects.count()
    not_voted = total_users - voted_users
    fig4, ax4 = plt.subplots()
    ax4.pie([voted_users, not_voted], labels=["Voted", "Not Voted"], autopct='%1.1f%%')
    ax4.set_title("Voter Turnout")
    chart4 = generate_base64_chart(fig4)

    # Clean up to avoid memory issues
    plt.close(fig1)
    plt.close(fig2)
    plt.close(fig3)
    plt.close(fig4)

    response = render(request, 'voting_sessions/session_charts.html', {
        'title': session.title,
        'session_end_time': session.session_end_time,
        'session_id': session.id,
        'outdated': timezone.now() > session.session_end_time,
        'active': session.is_voting_active,
        'timestamp': timezone.now(),
        'chart1': chart1,
        'chart2': chart2,
        'chart3': chart3,
        'chart4': chart4,
    })
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


# @login_required
# def results(request, session_id):
#     session = get_object_or_404(Session, id=session_id)
#     context = {
#         'session_id': session_id,  # pass session_id explicitly
#         # other data you want to pass to template
#     }
#     # return render(request, 'voting_sessions/session_charts.html', context)
#     return render(request, "session_charts.html", {"session": session})

def session_invite(request, session_uuid):
    """Handle invitation links and redirect users to the session page."""
    session = get_object_or_404(Session, uuid=session_uuid)

    if not request.user.is_authenticated:
        return redirect(f"{reverse('login')}?next={session.get_invite_link()}")

    return redirect('voting_sessions:session_detail', session_id=session.id)

def session_list(request):
    """Display a list of all voting sessions with preloaded options."""
    sessions = Session.objects.prefetch_related('options')
    return render(request, "session_list.html", {"sessions": sessions})


def session_invite(request, session_uuid):
    """Handle invitation links and redirect users to the session page."""
    session = get_object_or_404(Session, uuid=session_uuid)

    if not request.user.is_authenticated:
        return redirect(f"{reverse('login')}?next={session.get_invite_link()}")

    return redirect('voting_sessions:session_detail', session_id=session.id)

def session_list(request):
    """Display a list of all voting sessions with preloaded options."""
    sessions = Session.objects.prefetch_related('options')
    return render(request, "session_list.html", {"sessions": sessions})

@login_required
def session_detail(request, session_id):
    session = get_object_or_404(Session, id=session_id)

    if request.user.is_authenticated:
        SessionAccess.objects.update_or_create(
            user=request.user,
            session=session,
            defaults={'accessed_at': timezone.now()}
        )
    """Display details of a specific voting session."""
    session = get_object_or_404(Session.objects.prefetch_related('options'), id=session_id)
    return render(request, "session_detail.html", {"session": session})

@login_required
def vote(request, session_id):
    """Allow a user to cast a vote in an active session."""
    session = get_object_or_404(Session.objects.prefetch_related('options'), id=session_id)

    now = timezone.now()
    if now < session.voting_start_time:
        messages.error(request, "Voting is not allowed because the session hasn't started yet.")
        return redirect('voting_sessions:session_detail', session_id=session_id)
    elif now > session.session_end_time:
        messages.error(request, "Voting is not allowed because the session has ended.")
        return redirect('voting_sessions:session_detail', session_id=session_id)

    options = {option.id: option for option in session.options.all()}

    if request.method == 'POST':
        option_id = request.POST.get('option')

        if not option_id:
            messages.error(request, "Please select an option before submitting your vote.")
            return redirect('voting_sessions:session_detail', session_id=session_id)

        try:
            option_id = int(option_id)
            option = options.get(option_id)
        except (ValueError, TypeError):
            messages.error(request, "Invalid option selected.")
            return redirect('voting_sessions:session_detail', session_id=session_id)

        if not option:
            messages.error(request, "Selected option does not exist.")
            return redirect('voting_sessions:session_detail', session_id=session_id)

        existing_vote = Vote.objects.filter(user=request.user, session=session).first()
        if existing_vote:
            messages.error(request, "You have already voted in this session.")
        else:
            try:
                Vote.objects.create(user=request.user, option=option, session=session)
                messages.success(request, "Your vote has been cast successfully!")
            except ValidationError as e:
                messages.error(request, f"Error: {e}")

        return redirect('voting_sessions:session_charts', session_id=session_id)

    return render(request, 'vote/vote.html', {'session': session, 'options': options.values()})

def session_list(request):
    sessions = Session.objects.all()
    return render(request, 'voting_sessions/session_list.html', {'sessions': sessions})


