from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from matplotlib import pyplot as plt
from django.db.models import Count
from django.db.models.functions import TruncMinute
from voting_sessions.models import Session, Option
from vote.models import Vote
import os

class Command(BaseCommand):
    help = 'Generate static chart images for documentation'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--session_id',
            type=int,
            help='ID of the session to generate charts for'
        )

from django.core.management.base import BaseCommand
from django.utils.timezone import localtime
from django.db.models.functions import TruncMinute
from django.db.models import Count
from voting_sessions.models import Session, Option
from django.contrib.auth import get_user_model
import matplotlib.pyplot as plt
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Generate chart images for a given session'

    def add_arguments(self, parser):
        parser.add_argument('--session_id', type=int, help='Session ID to generate charts for')

    def handle(self, *args, **options):
        session_id = options.get('session_id')
        if not session_id:
            self.stderr.write(self.style.ERROR('Please provide a session_id using --session_id'))
            return

        session = Session.objects.get(id=session_id)
        options_qs = Option.objects.filter(session=session)
        votes = [opt.votes.count() for opt in options_qs]
        names = [opt.title for opt in options_qs]
        filtered_labels = [name if vote > 0 else '' for name, vote in zip(names, votes)]

        # Line chart data
        votes_by_time = (
            Vote.objects.filter(session=session)
            .annotate(minute=TruncMinute('created_at'))
            .values('minute')
            .annotate(vote_count=Count('id'))
            .order_by('minute')
        )
        timestamps = [v['minute'] for v in votes_by_time]
        counts = [v['vote_count'] for v in votes_by_time]
        cumulative_counts = [sum(counts[:i+1]) for i in range(len(counts))]

        output_dir = 'docs/assets/images'
        os.makedirs(output_dir, exist_ok=True)

        # Bar chart
        fig1, ax1 = plt.subplots()
        ax1.bar(names, votes)
        ax1.set_title("Votes per Option")
        fig1.savefig(os.path.join(output_dir, 'bar_chart.png'))
        plt.close(fig1)

        # Pie chart
        fig2, ax2 = plt.subplots()
        ax2.pie(votes, labels=filtered_labels, autopct=lambda p: f'{p:.1f}%' if p > 0 else '')
        ax2.set_title("Vote Percentages")
        fig2.savefig(os.path.join(output_dir, 'pie_chart.png'))
        plt.close(fig2)

        # Line chart
        fig3, ax3 = plt.subplots()
        ax3.plot(timestamps, cumulative_counts, marker='o')
        ax3.set_title("Voting Activity Over Time")
        ax3.set_xlabel("Time")
        ax3.set_ylabel("Votes")
        plt.setp(ax3.get_xticklabels(), rotation=45, ha='right')
        fig3.tight_layout()
        fig3.savefig(os.path.join(output_dir, 'line_chart.png'))
        plt.close(fig3)

        # Turnout chart
        voted_users = Vote.objects.filter(session=session).values('user').distinct().count()
        total_users = User.objects.count()
        not_voted = total_users - voted_users
        fig4, ax4 = plt.subplots()
        ax4.pie([voted_users, not_voted], labels=["Voted", "Not Voted"], autopct='%1.1f%%')
        ax4.set_title("Voter Turnout")
        fig4.savefig(os.path.join(output_dir, 'turnout_chart.png'))
        plt.close(fig4)

        self.stdout.write(self.style.SUCCESS(f'Charts for session {session_id} saved in docs/assets/images/'))

