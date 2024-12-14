from voting_sessions.models import Session
from datetime import timedelta, datetime
from datetime import datetime, timezone

utc_time = datetime.now(timezone.utc)
session_start_time = utc_time
choice_duration = timedelta(days=15)  # Number of days
voting_duration = timedelta(days=5)
sum = session_start_time + choice_duration + voting_duration
print(sum)