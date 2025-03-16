@echo off
cd /d C:\VS_Code\Camp_programs\Projects\vote_cast
call venv\Scripts\activate
python manage.py send_notifications
