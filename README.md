# Creating a Google Tasks CLI in Python

## References

https://developers.google.com/docs/api/quickstart/python

## Notes

create a new project in google cloud

i created `got-cli`:

then search in the apis services section of the cloud console and enable:

* google docs api
* google tasks api

configure oauth consent by going to apis & services => oauth consent screen

named it Got CLI
user type external
no domains
skip adding scopes
add yourself as a test user

now need to add credentials for a desktop app
create credentials => oauth client ID
application type => desktop app
name it (i named it "Got CLI")
create => ok

output:
```
Client ID
<redacted>

Client secret
<redacted>

Creation date
July 26, 2023 at 1:46:07 PM GMT-4

Status
Enabled 
```

look for the new creds under "oauth 2.0 client IDs"

save downloaded JSON file to `credentials.json` in your project working dir

```
mv ~/Downloads/client_secret_STUFF.json ~/src/got-cli/credentials.json
```

```
pipenv install \
    google-api-python-client \
    google-auth-httplib2 \
    google-auth-oauthlib
```

```
got tasklists list
got tl l
got tl set
got tl s 3
got tasks list 
got t list
got t l
got tasks list --tasklist 
got t l 




