# google_api.py
# Developed using: https://developers.google.com/gmail/api/guides/drafts

import base64
from email.message import EmailMessage
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

from google_auth import Google_Auth

class Google_Api:
    '''
    Class for abstracting the use of the Google API.
    '''

    google_auth = None

    def __init__(self,token_path: str,credentials_path: str, scopes: list[str]):
        self.google_auth = Google_Auth(token_path=token_path
                                       ,credentials_path=credentials_path
                                       ,scopes=scopes)
        self.send_email(to=['kstine93+tes@gmail.com'],
                        subject="test_sub"
                        ,email="test this email!!"
                        )

    #---------------
    def test_creds(self):
        #Have basic test to confirm with Google that the credentials and the scope match + are ready for usage in API.
        try:
            # Call the Gmail API
            service = build('gmail', 'v1', credentials=self.creds)
            results = service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])

            if not labels:
                print('No labels found.')
                return
            print('Labels:')
            for label in labels:
                print(label['name'])

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')

    #---------------
    def send_email(self, to: list[str], subject: str, email: str = None, email_html: str = None, cc: list[str]=None,):
        if email and email_html:
            raise ValueError("Please specify either an email string or email_html - but not both")
        
        try:
            service = build('gmail', 'v1', credentials=self.google_auth.get_creds())

            message = EmailMessage()
            message.set_content(email)
            message['To'] = to
            message['From'] ='kstine93@gmail.com' #Do I have to set this?
            message['Subject'] = subject

            # encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            create_message = {
                'message': {
                    'raw': encoded_message
                }
            }

            draft = service.users().drafts().create(userId="me",
                                                    body=create_message).execute()

            print(F'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')

            return draft
        
        except HttpError as error:
            #TODO: Find way to re-try connection if a failure happens
            #The issue here is that while we can see if we get a 403 error indicating a mis-match between credentials and a token,
            #we don't know what scope is needed to satisfy this. Maybe we can change the SCOPE again manually here?
            print(f'An error occurred: {error}')

            if(error.status_code == 403):
                self.warn_scopes(['https://www.googleapis.com/auth/gmail.compose'])

    
        #NOTE: If I get a 403 error, this is the perfect time to try to re-load the token!

        #if email, send with email string
        #elif email_html, send with email html
        #if email and email_html both none, raise an error

        #Once email successfully sent, return success code from Google API? Or don't expose this and return nothing?

    def search_email_threads(search_str: str):
        pass
        #Ask Google API to return threads (or conversations?) that match the search str. Return this to the user more-or-less raw.
        #Note: Need to have good error handling in case there are mistakes in the search_str (would be pretty common)
    
    def warn_scopes(self,new_scopes: list[str]):
        print("Authentication error. Please add the following scopes and attempt to use the endpoint again.\nScopes:")
        for scope in new_scopes:
            print(scope)
        # self.google_auth.append_to_scope(new_scope)

if __name__ == "__main__":
    base_dir = "/home/rambino/.gcp"
    scopes = ['https://www.googleapis.com/auth/gmail.readonly'
              ,'https://www.googleapis.com/auth/gmail.readonly']
    t = Google_Api(token_path=base_dir+"/token.json"
                    ,credentials_path=base_dir+"/credentials.json"
                    ,scopes=scopes)