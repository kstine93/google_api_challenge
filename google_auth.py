# google_auth.py
# Developed using code from: https://developers.google.com/gmail/api/quickstart/python

#---------------

from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

#---------------
class Google_Auth:
    '''
    Class for authenticating a local application with a Google Cloud Project and storing credentials
    to enable later API calls.

    To learn more about the scopes you can use for Google API calls, see here:
    https://developers.google.com/identity/protocols/oauth2/scopes
    '''

    #credentials stored locally are used for API calls
    creds = None

    #scopes are embedded in a token. Different scopes need a different token
    scopes = None
    prev_scope_path = "./current_google_scopes.txt"

    cred_path = None
    token_path = None

    #---------------
    def __init__(self
                 ,scopes: list[str]
                 ,token_path: str = "./token.json"
                 ,credentials_path: str = "./credentials.json"
                 ):

        self.cred_path = credentials_path
        self.token_path = token_path
        self.scopes = scopes

        #If previous and new scopes do not match, re-load credentials to prevent issues.
        scopes_match = set(self.read_previous_scope()) == set(scopes)
        if not scopes_match:
            self.load_or_refresh_token()
            self.write_previous_scope(scopes)
        
        else:
            if os.path.exists(self.token_path):
                self.creds = Credentials.from_authorized_user_file(self.token_path, self.scopes)

            if not self.creds or not self.creds.valid or not scopes_match:
                self.load_or_refresh_token()

    #---------------
    def get_creds(self):
        return self.creds
    
    #---------------
    def delete_token_file(self):
        os.remove(self.token_path)

    #---------------
    def read_previous_scope(self):
        with open(self.prev_scope_path, "r") as file:
            return file.read().splitlines()

    #--------------- 
    def write_previous_scope(self,scope):
        with open(self.prev_scope_path, "w") as file:
            file.write("\n".join(scope))

    #---------------
    def load_or_refresh_token(self):        
        if self.creds and self.creds.expired and self.creds.refresh_token:
            self.__refresh_credentials()
        else:
            self.__login_to_google()
        # Save the credentials for the next run
        self.__store_credentials_local()

    #---------------
    def __refresh_credentials(self):
        self.creds.refresh(Request())

    #---------------
    def __login_to_google(self):
        print("NOTE: The OAuth token for this app is either missing or needs to be updated with a different scope.\n")
        flow = InstalledAppFlow.from_client_secrets_file(
            self.cred_path, self.scopes)
        self.creds = flow.run_local_server(port=0)

    #---------------
    def __store_credentials_local(self):
        #method for abstracting the storage of credentials in a local file
        #this is the easiest method, but might not be the most secure.
        #In the future, we could make other methods to store offsite (e.g., in remote database)
        with open(self.token_path, 'w') as file:
            file.write(self.creds.to_json())

#---------------