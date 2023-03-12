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

    def __init__(self,token_path,credentials_path):
        self.google_auth = Google_Auth(token_path=token_path,credentials_path=credentials_path)
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
        # pylint: disable=E1101
        draft = service.users().drafts().create(userId="me",
                                                body=create_message).execute()

        print(F'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')

        return draft
    
        #NOTE: If I get a 403 error, this is the perfect time to try to re-load the token!

        #if email, send with email string
        #elif email_html, send with email html
        #if email and email_html both none, raise an error

        #Once email successfully sent, return success code from Google API? Or don't expose this and return nothing?

    def search_email_threads(search_str: str):
        pass
        #Ask Google API to return threads (or conversations?) that match the search str. Return this to the user more-or-less raw.
        #Note: Need to have good error handling in case there are mistakes in the search_str (would be pretty common)
    

if __name__ == "__main__":
    base_dir = "/home/rambino/.gcp"
    t = Google_Api(token_path=base_dir+"/token.json"
                    ,credentials_path=base_dir+"/credentials.json")