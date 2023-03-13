# gmail_api.py
# Developed using code from: https://developers.google.com/gmail/api/guides/drafts

#---------------

import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google_auth import Google_Auth

#---------------
class Gmail_Api:
    '''
    Class for abstracting the use of the Gmail API.
    Documentation on Gmail API:
    https://developers.google.com/gmail/api/guides
    '''
    #---------------
    google_auth = None

    #---------------
    def __init__(self,google_auth: Google_Auth):
        #Loading credentials to use API
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
            return send_message
        
        except HttpError as error:
            print(f'An error occurred: {error}')

    #---------------
    def search_email_get_one_page(self, search_str:str, pageToken:str|None=None):
        try:
            service = build('gmail', 'v1', credentials=self.google_auth.get_creds())
            msg_service = service.users().messages()
            response = msg_service.list(userId="me",q=search_str,pageToken=pageToken).execute()
            return response

        except HttpError as error:
            print(f'An error occurred: {error}')

    #---------------
    def search_email_get_all_messages(self, search_str: str):
        response = self.search_email_get_one_page(search_str)
        messages = response['messages'] if 'messages' in response else []

        while 'nextPageToken' in response:
            response = self.search_email_get_one_page(search_str, pageToken=response['nextPageToken'])
            messages.extend(response['messages'] if 'messages' in response else [])

        return messages
    
#---------------