#Gmail Api Challenge - Quickstart

#---------------
from google_auth import Google_Auth
from gmail_api import Gmail_Api

#---------------
#-INITIAL SETUP-
#---------------
#At this point, you should have created your Google Cloud Project (GCP) and downloaded your OAuth credentials.
#See the README document for instructions on how to do this.

#Change this value to be the file path and name of YOUR OAuth credentials file (must be JSON format).
credentials_path = "/home/rambino/.gcp/credentials.json"

#Where your OAuth token should be stored. This will be created the first time you run the application.
#(suggestion: put this in the same folder as your credentials):
token_path = "/home/rambino/.gcp/token.json"

#Scopes- what your OAuth token is allowed to do in your GCP. The 2 provided by default below will allow you to
#read and search the emails in your Gmail account, as well as compose & send emails.
scopes = ['https://www.googleapis.com/auth/gmail.compose'
          ,'https://www.googleapis.com/auth/gmail.readonly']

#----------------
#--STARTING APP--
#----------------
#Ask Google to give you a OAuth token based on your existing credentials and your desired scope.
#NOTE: Creating a token will require you to follow a link in this application's output and log into
#your Google account.
auth = Google_Auth(token_path = token_path
                ,credentials_path = credentials_path
                ,scopes = scopes)

#Preparing our Gmail API connection
gmail = Gmail_Api(auth)

#---------------
#--SEND EMAILS--
#---------------
#Use the template below to write your own emails and send them.
body = "<h2>Congratulations!</h2><p>Kevin, we would be delighted to offer you a position on our team.</p>"

sent_message = gmail.send_email(to=['kstine93@gmail.com']
                                ,subject="Welcome to Haensel AMS!"
                                ,body=body
                                ,body_is_html=True
                                ,cc=[]
                                )

print(f"Sent message with ID: {sent_message['id']}")

#---------------
#-SEARCH EMAILS-
#---------------
#Use the template below to search for emails in your Gmail inbox.
#Note that this will only return email thread IDs which match your search criteria.
#Functionality to pull in the actual messages from these IDs is still a WIP.
#For more information on writing these search strings, see here:
#https://developers.google.com/gmail/api/guides/filtering
messages = gmail.search_email_get_all_messages(search_str="from:kstine93@gmail.com after:2023/03/05")
print(f"Gmail found {len(messages)} messages fitting your search.")
