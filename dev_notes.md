# google_api_challenge
This repo is for a challenge undertaken as a test for a Data Engineering position, originally found at this link: https://github.com/haensel-ams/recruitment_challenge/tree/master/DevOps_201909

This file contains development notes to show more how this app was created and the decisions that went into it.


---

## Details of the challenge:

### Goal:
- setup a test gmail account and enable the APIs for it
- cover the following features:
  - send emails
  - search for specific messages in the mailbox, e.g. for keywords in subject or body text
- a brief documentation of your steps in terms what is needed to setup this API connection, PLEASE in your words not just copy & paste from google


### Remarks:
- well commented and easy to follow code
- please use only Python
- also a plus is to show some programming skills by using: classes, functions, etc.
- provide us runnable code !

---

## Notes & planning:

### Google API:
The Google API looks relatively simple, except for its authentication system. Using the Google API requires:
- Creation of a Google Cloud project: https://developers.google.com/workspace/guides/create-project
- Enablement of API from GCP (requires using web interface? If yes, need to provide instructions on how to do this).
- Create OAuth client ID (note: one for each app necessary) from the GCP project
- Installing Google Client library (use virtual env? Might be bulky, knowing Google): https://developers.google.com/gmail/api/quickstart/python
- Have the app 'handshake' with Google by providing credentials and a desired scope - only THEN will Google transfer the actual token(s?) which can be used in API calls
  - Note: If scope ever needs to change, handshake needs to happen again: https://developers.google.com/gmail/api/quickstart/python

Note that Google requires storing *credential JSONs* as a way of authenticating rather than a more conventional *string*. So depending on the environment, I might have to be thoughtful on how I store these.

>More resources on Google authentication: https://developers.google.com/workspace/guides/auth-overview


### Architecture:

#### Credential Setup:
Credential setup might be the biggest part of the project - since it requires some manual setup with creating a GCP + handshaking with Google.
I might want to have that process be completely separate - it should only be 1-time (unless rotation is needed) and has no relevance to the rest of the app.
>Why don't I configure this as a set of two classes: one for authentication and another for API calls? I like keeping them separate - in case one changes, I don't have to fiddle with the other one.

#### API usage:
Since the API is already pretty usable, my implementation can focus on making a nice abstracted layer for the user.
Some ideas:
- Send Email:
  - How about a simple version with just a string `SUBJECT_LINE` and `BODY_TEXT` and then an advanced version that can use HTML files?
    - Take a look at the API used for Apps Script - that abstraction is quite nice already.
- Search for messages (body or subject):
  - See the guide Google has here: https://developers.google.com/gmail/api/guides/filtering
  - There are a lot of expansions we could make for the search: https://support.google.com/mail/answer/7190
  - I think a nice but extensible place to start would be to just accept a string using Google's search syntax and just pass that along to Google. This is really basic, but with enough examples (and Google has its own good documentation), this would be the most flexible implementation. We could then wrap this in another layer later which makes the search query for you in a more user-friendly way





