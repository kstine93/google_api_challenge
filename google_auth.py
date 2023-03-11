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
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



#---------------

class google_auth:
    '''
    Class for authenticating a local application with a Google Cloud Project and storing credentials
    to enable later API calls.
    '''

    #credentials stored locally are used for API calls
    creds = None

    #DO I NEED THESE JSON VERSIONS?
    cred_json = {}
    token_json = {}

    # If modifying these scopes, delete the file token.json
    scopes = ['https://www.googleapis.com/auth/gmail.readonly']

    cred_path = ""
    token_path = ""

    #---------------
    def __init__():
        #Do I need users to send me the credentials_json? That seems silly...
        #Maybe an easier way to configure where the credentials are stored?

        #How can I 'remember' the scopes between runs? It seems that Google is already checking if the tokens match the scope.
        #can I just look for an error for Google about a mis-match and if so, re-load the token?
        #e.g., "Detected scope change from previous run - re-initializing token..."
        pass

    def change_scopes(self,new_scope_list: list[str]):
        pass
        #1. if new scopes are different than old (compare sets), then:
        #   a. delete token (local values and file) and then:
        #       i. get_token
        #       

    def get_creds(self):
        return self.creds
    
    def test_creds(self):
        #Have basic test to confirm with Google that the credentials and the scope match + are ready for usage in API.
        pass

    #---------------
    def __load_or_refresh_token(self,token_path):
        # if os.path.exists(token_path):
        #     self.creds = Credentials.from_authorized_user_file(token_path, self.scopes)
        # #If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                self.__refresh_credentials()
            else:
                self.__login_to_google()
            # Save the credentials for the next run
            self.__store_credentials_local(token_path)
 
    #---------------
    def __refresh_credentials(self):
        self.creds.refresh(Request())

    #---------------
    def __login_to_google(self):
        '''Prompt user to login to their GCP account - to re-allocate credentials.'''
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', self.scopes)
        self.creds = flow.run_local_server(port=0)

    #---------------
    def __store_credentials_local(path):
        #method for abstracting the storage of credentials in a local file
        #this is the easiest method, but might not be the most secure.
        #In the future, we could make other methods to store offsite (e.g., in remote database)
        pass
        #1. Save to path
        # with open(token_path, 'w') as token:
        #     token.write(creds.to_json())

        #2. self.credentials_path = path


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