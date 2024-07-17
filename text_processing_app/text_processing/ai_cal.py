import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from phi.assistant import Assistant
from phi.llm.ollama import Hermes
import os

# refresh token.json if scopes get changed
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
        token.write(creds.to_json())

def find_gcal_events_day(day:int, month: int, year: int):
    """
    Finds Gcal events of user
    :param day: the day of the event
    :param month: the month of the event
    :param year: the year of the event
    :return: a string of all events the LLM can process
    """

    try:
        service = build("calendar", "v3", credentials=creds)
        # Call the Calendar API
        print("Getting the events for today")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=f'{year}-{month}-{day}T00:00:00-07:00',
                timeMax=f'{year}-{month}-{day}T23:59:00-07:00',
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return "No events were found"

        # Prints the start and name of the next 10 events
        return_str = f"There are {len(events)} events for that day: "
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])
            return_str += f"{event['summary']} - {event['description']} at {start}, "
        return return_str
    except HttpError as error:
        print(f"An error occurred: {error}")


def make_gcal_event(day:int, month: int, year: int, title: str, description: str, hour: int, minute: int):
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
          token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        event = {
            'summary': title,
            'description': description,
            'start': {
                'dateTime': f'{year}-{month}-{day}T{hour}:{minute}:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': f'{year}-{month}-{day}T{hour}:{minute}:00-07:00',
                'timeZone': 'America/Los_Angeles',
            }
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))
        return 'Event created: %s' % (event.get('htmlLink'))


    except HttpError as error:
        print(f"An error occurred: {error}")
        return f"An error occurred: {error}"


def run_assistant(prompt):
    assistant = Assistant(
        tools=[find_gcal_events_day, make_gcal_event],
        show_tool_calls=False,
        llm=Hermes(model="adrienbrault/nous-hermes2pro:Q8_0"),
        description="You are a secretary assistant who provides helpful and concise information about the user's calendar. Use find_gcal_events_day to find events for one day, and make_gcal_event to make a calendar event.")
    # show me whats happening on 1, 4, 2025
    # Runs the LLM with the prompt from the user
    response = assistant.run(prompt, stream=False)
    return response
response = run_assistant("show me whats happening on April 1 2025")
print("Below is the response:")
print(response)


