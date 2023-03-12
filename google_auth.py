# google_auth.py
# TODO: implement class here which authenticates with Google and stores credentials locally (or in designated location)
# NOTE: authentication can happen asynchronously from API calls.
# NOTE: Much of the code below was adapted from Google's Python quickstart: https://developers.google.com/gmail/api/quickstart/python

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
    '''

    #credentials stored locally are used for API calls
    creds = None

    # If modifying these scopes, delete the file token.json
    scopes = None

    cred_path = None
    token_path = None

    #---------------
    def __init__(self,token_path: str,credentials_path: str, scopes: list[str]):

        #TODO: Figure out if where I want default values for the credentials + tokens to be - or maybe not default values at all.
        self.cred_path = credentials_path
        self.token_path = token_path
        self.scopes = scopes

        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, self.scopes)

        if not self.creds or not self.creds.valid:
            self.load_or_refresh_token()

        #Do I need users to send me the credentials_json? That seems silly...
        #Maybe an easier way to configure where the credentials are stored?

        #How can I 'remember' the scopes between runs? It seems that Google is already checking if the tokens match the scope.
        #can I just look for an error for Google about a mis-match and if so, re-load the token?
        #e.g., "Detected scope change from previous run - re-initializing token..."
        #NOTE: Changing the scope alone does not trigger an error - maybe we need to call the service too?
        #NOTE: Yep. If we do something outside the scope, we get a 403 error- a good opportunity to try to re-load the token.

    #---------------
    def get_creds(self):
        return self.creds

    #---------------
    def load_or_refresh_token(self):        
        if self.creds and self.creds.expired and self.creds.refresh_token:
            self.__refresh_credentials()
        else:
            self.__login_to_google()
        # Save the credentials for the next run
        self.__store_credentials_local()

    #def append_to_scope(self,new_scopes: list[str]):

 
    #---------------
    def __refresh_credentials(self):
        #TODO: Test this 
        self.creds.refresh(Request())

    #---------------
    def __login_to_google(self):
        '''Prompt user to login to their GCP account - to re-allocate credentials.'''
        flow = InstalledAppFlow.from_client_secrets_file(
            self.cred_path, self.scopes)
        self.creds = flow.run_local_server(port=0)

    #---------------
    def __store_credentials_local(self):
        #method for abstracting the storage of credentials in a local file
        #this is the easiest method, but might not be the most secure.
        #In the future, we could make other methods to store offsite (e.g., in remote database)
        pass
        #1. Save to path
        with open(self.token_path, 'w') as file:
            file.write(self.creds.to_json())

'''
Configurable options in this class:
1. Paths of credentials
2. Scope of credentials

Things people can do:
1. Change scope
2. Get credentials
3. Test credentials

Things that this class needs to do on its own:
1. Load in credentials from given path
2. Prompt user for login if credentials are invalid
3. Save credentials to given path
'''

if __name__ == "__main__":
    base_dir = "/home/rambino/.gcp"
    t = Google_Auth(token_path=base_dir+"/token.json"
                    ,credentials_path=base_dir+"/credentials.json")