@echo off
echo Script started at %DATE% %TIME% >> C:\VS_Code\Camp_programs\Projects\vote_cast\notifications_log.txt
cd /d C:\VS_Code\Camp_programs\Projects\vote_cast
echo Running Python script... >> C:\VS_Code\Camp_programs\Projects\vote_cast\notifications_log.txt
venv\Scripts\python.exe manage.py send_notifications >> C:\VS_Code\Camp_programs\Projects\vote_cast\notifications_log.txt 2>&1
echo Script finished at %DATE% %TIME% >> C:\VS_Code\Camp_programs\Projects\vote_cast\notifications_log.txt
