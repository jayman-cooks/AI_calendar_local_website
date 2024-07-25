# Local AI Calendar Helper Server
This project allows you to host a server that will allow anyone on your network to access an AI helper! This is **only** made to be a local server.


## Installing
1. Install packages from requirements.txt.
2. Inside of DJ_server_calendar, you need to add 3 files containing credentials.
    - `django_secret.json`: Your django secret key. You can probably just generate a new one
    - `openai_tok.json`: Your hackclub openai wrapper key. 
    - `credentials.json`: Follow this guide until you download the credentials: https://developers.google.com/calendar/api/quickstart/python/ (rename it too). Also add your google account as a test user (or you will get an access denied error).
3. Figure out your ip. There are many websites or commands to do this. Add it to testing_tailwinds/settings.py. 
4. Run the server with
```bash
python manage.py runserver YOUR_IP_HERE:8000
```
Click on the link it gives you. The first time you run the assistant, it will make you complete authorization. Copy the file it makes to the same directory as manage.py
## Functions
There are currently two functions the assistant has access to. 
1. Reading events: day, month, and year of the event(s).
2. Creating events: day, month, year, title, description, and time of the event to create.
The assistant needs to be provided with all of the inputs. 