import os.path

import click
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from rich.console import Console
from rich.markdown import Markdown
from rich.pretty import pprint
from rich.table import Table
from rich.text import Text

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/documents.readonly',
    'https://www.googleapis.com/auth/tasks.readonly',
]

# The ID of a sample document.
# DOCUMENT_ID = '195j9eDD3ccgjQRttHhJPymLJUCOUjs-jmwTrekvdjFE'
DOCUMENT_ID = '1KD-zOc9-g3WW3ieBhqDIdXqoYxux39ImbUFuXvjXQlc'

TASKLIST_ID = 'MTU2MjgyMTY3MjczMjI1NTQxOTQ6MDow'

@click.group()
@click.pass_context
def cli(context):
    context.ensure_object(dict)
    creds = auth()
    context.obj['creds'] = creds
    context.obj['service'] = build('tasks', 'v1', credentials=creds)
    context.obj['console'] = Console()


@cli.group(name='tl')
@click.pass_context
def tl(_context):
    pass


@tl.command(name='list')
@click.pass_context
def list_(context):
    tasklists_list(context)


@tl.command()
@click.pass_context
def l(context):
    tasklists_list(context)


@cli.group()
@click.pass_context
def t(_context):
    pass

@t.command()
@click.pass_context
def l(context):
    tasks_list(context)


def tasklists_list(context):
    service = context.obj['service']
    response = service.tasklists().list(maxResults=10).execute()
    print(response)
    table = Table(title="Task Lists")
    table.add_column("Number")
    table.add_column("Title")
    table.add_column("ID")
    for i, tl in enumerate(response.get('items', [])):
        table.add_row(str(i), tl['title'], tl['id'])
        # print(tl['title'], tl['id'])
    console = context.obj['console']
    console.print(table)


def tasks_list(context):
    service = context.obj['service']
    response = service.tasks().list(tasklist=TASKLIST_ID, maxResults=10).execute()
    pprint(response)
    table = Table(title="Tasks")
    table.add_column("Number")
    table.add_column("Status")
    table.add_column("Title")
    table.add_column("ID")
    console = context.obj['console']
    for i, t in enumerate(response.get('items', [])):
        task_response = service.tasks().get(tasklist=TASKLIST_ID, task=t['id']).execute()
        pprint(task_response)
        console.print(Markdown(task_response['notes']))
        status = t['status']
        status_style = ''
        status_text = status
        if status == 'needsAction':
            status_style = 'purple'
            status_text = Text('TODO', style=status_style)
        table.add_row(str(i), status_text, t['title'], t['id'])
    console.print(table)


def auth() -> Credentials:
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


if __name__ == '__main__':
    #main()
    cli()
