# google_api.py
# Developed using code from: https://developers.google.com/gmail/api/guides/drafts

import base64
from email.mime.text import MIMEText
from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google_auth import Google_Auth

class Google_Api:
    '''
    Class for abstracting the use of the Google API.
    '''
    #---------------
    google_auth = None

    #---------------
    def __init__(self,google_auth: Google_Auth):
        self.google_auth = google_auth

    #---------------
    def send_email(self, to: list[str], subject: str, body: str, body_is_html: bool = False, cc: list[str]=[]):
        
        mimeTextType = "html" if body_is_html else "plain"

        try:
            service = build('gmail', 'v1', credentials=self.google_auth.get_creds())

            message = MIMEText(body,mimeTextType)
            message['to'] = ", ".join(to)
            #message['from'] = sender #Not setting this - don't think it's needed.
            message['subject'] = subject
            message['cc'] = ", ".join(cc)

            # encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            message = {'raw':encoded_message}
            send_message = service.users().messages().send(userId="me", body=message).execute()
            print(f'MessageID: {send_message["id"]}')
        
        except HttpError as error:
            print(f'An error occurred: {error}')

    def search_email_threads(search_str: str):
        pass
        #Ask Google API to return threads (or conversations?) that match the search str. Return this to the user more-or-less raw.
        #Note: Need to have good error handling in case there are mistakes in the search_str (would be pretty common)


#---------------
if __name__ == "__main__":
    base_dir = "/home/rambino/.gcp"

    #This is probably too many scopes - whittle down once I know what I need:
    scopes = ['https://www.googleapis.com/auth/gmail.readonly'
              ,'https://www.googleapis.com/auth/gmail.compose'
              ,'https://www.googleapis.com/auth/gmail.send'
              ,'https://www.googleapis.com/auth/gmail.modify']
    auth = Google_Auth(token_path=base_dir+"/token.json"
                    ,credentials_path=base_dir+"/credentials.json"
                    ,scopes=scopes)
    
    t = Google_Api(auth)

    t.send_email(to=['kstine93+tes@gmail.com']
                    ,subject="test_sub"
                    ,body="test this email!!"
                    ,body_is_html=False
                    ,cc=[]
                    )