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

---

### Google Authentication System
Google offers multiple systems by which you can authenticate to use Google APIs. These vary in security, capabilities, and complexity to set up.

#### API keys
API keys are not particularly secure in the scope of authentication options - so we will avoid using them if possible.

[More information on authenticating with Google API keys](https://cloud.google.com/docs/authentication/api-keys)

---

#### Service Accounts
Service accounts are special accounts owned by applications rather than people. As opposed to OAuth, service accounts can be used by multiple people.
However, Service accounts are not allowed to access certain APIs that require impersonating a particular user (e.g., the Gmail API) without enabling **"domain-wide delegation"** for the service account - which can only be done with a Google Workspace account - which costs money.

Since this paying option is also beyond our scope, we will not use this option.
Additionally, there was some indication that Google Workspace APIs (e.g., Gmail,Drive) should not be accessed via Service Accounts anyway, since these resources are deeply tied to individual users - and so user-based authentication is more appropriate.

---

#### OAuth 2.0 Client IDs
OAuth client IDs allow end users to simply use their Google login credentials as a way to authenticate.
This appears to be designed mostly for use in user-focused Apps where integration with a user's Google account is necessary (e.g., "login with Google"?).
There are some options that you need to leave blank (particularly 'scopes') in order to not require a Google review. [This video](https://www.youtube.com/watch?v=IV3PN7IejTg) provides a nice walkthrough.

**This is the authentication method we should use.**

[More OAuth information from Google](https://developers.google.com/workspace/guides/create-credentials#oauth-client-id)

---

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

---

### Steps
- [X] Design BASIC version of my app - so that I can just see where I'll put everything (pseudocode fine)
  - [X] google_auth authorisation class (manages connection to Google, re-authentication if sth fails)
  - [X] google_api api abstraction class (provides methods to connect to Google API); keeps complexity nicely contained
  - [ ] quickstart.py (demonstrates how to use classes to do operations mentioned in **GOAL**)
- [X] Create GCP + set up authentication
- [X] Set up environment (use virtual environment with requirements.txt to allow anyone to download + use the code).
- [X] Build out code more
  - [X] Build out google_auth with actual code
  - [X] Test google_auth
  - [X] Build out google_api with actual code
  - [X] Test google_api
  - [X] Build quickstart.py (should be very easy once testing is complete)
- [ ] Refine documentation:
  - [ ] Build out README to show how to boot up app + work with GCP


---

## DEVELOPMENT NOTES

> **Mar. 12, 2023:**
> I finally got the OAuth working - it's pretty graceful in that Google simply asks for permission the browser- and only once.
> But the token it gives you is pretty odd - it is monolithic for a specific scope. And any additional scopes will return a 403.
> TODO:
> [X] Build out email search functionality
> 2. Figure out way that Auth class can identify when scope has changed (keep local file which has existing scope?) so that if scope changes, then it automatically tries to reset token - before any issues happen in the API calls.
> 3. Clean up code + documentation
> 4. Done!