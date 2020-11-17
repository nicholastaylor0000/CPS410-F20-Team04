# HerokuScoreTrackerAPI
Paragalactic Leaderboard and Scheduler App - Setup Instructions 

Mentioned Installations 

Python v3.8.1: https://www.python.org/downloads/release/python-381/

Docker Desktop: https://hub.docker.com/editions/community/docker-ce-desktop-windows/ 

Docker Desktop (MAC): https://hub.docker.com/editions/community/docker-ce-desktop-mac/ 

Upon Paul’s Recommendation: Postman: https://www.postman.com/downloads/ 

Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli 

Git (required by Heroku CLI) : https://git-scm.com/downloads 

C++ Build Tools (Error comes up for Twisted if you do not have this already installed, comes with many other programs so may already have a version of this): https://visualstudio.microsoft.com/visual-cpp-build-tools/ 

SETUP:

Clone HerokuScoreTrackerAPI onto Local Machine
Make sure to also swap from the master branch to team04. If you want, you can also make a branch off of this branch when you push changes just to ensure you do not mess with what others are doing as you can then push that branch to our branch but TL:DR do not push our branch into master

Using either Visual Studio Code PowerShell terminal or terminal application of choice, follow steps below. You can also make git changes from Visual Studio Code so in bottom left mind what branch you are in.
python -m venv venv -> python virtual environment
MAC:: “source <DIR>/bin/activate”  - WINDOWS :: “.\venv\Scripts\activate”
“pip install –r requirements.txt”
docker-compose up -d
"python manage.py migrate"
“python manage.py createsuperuser” - to access django admin from local client
"python manage.py runserver"
Ctrl+c to stop server while running in Terminal


