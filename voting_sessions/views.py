# voting_sessions/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Session
# from .tasks import notify_session_start, schedule_voting_reminder
from datetime import timedelta

def session_list(request):
    sessions = Session.objects.all()
    return render(request, "session_list.html", {"sessions": sessions})

def session_detail(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    return render(request, "session_detail.html", {"session": session})

def create_session(request):
    if request.method == "POST":
        # Simplified form handling
        title = request.POST.get("title")
        description = request.POST.get("description")
        session_start_time = request.POST.get("session_start_time")  # Ensure valid datetime format
        choice_duration = int(request.POST.get("choice_duration"))
        voting_duration = int(request.POST.get("voting_duration"))

        session = Session.objects.create(
            title=title,
            description=description,
            session_start_time=session_start_time,
            choice_duration=choice_duration,
            voting_duration=voting_duration
        )

        # Trigger Celery tasks
        notify_session_start.delay(session.id)
        schedule_voting_reminder.apply_async(
            args=[session.id],
            eta=session.session_start_time + timedelta(days=choice_duration - 1)
        )

        return redirect("voting_sessions:session_list")
    return render(request, "create_session.html")
