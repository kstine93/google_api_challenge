# google_api.py


class google_api:
    '''
    Class for abstracting the use of the Google API.
    '''

    creds = None

    def __init__(self):
        #1. Initialize google_auth instance
        #2. Get credentials from google_auth and store in class variables
        pass

    def send_email(to: list[str], cc: list[str], subject: str, email: str = None, email_html: str = None):
        if email and email_html:
            raise ValueError("Please specify either an email string or email_html - but not both")
        #if email, send with email string
        #elif email_html, send with email html
        #if email and email_html both none, raise an error

        #Once email successfully sent, return success code from Google API? Or don't expose this and return nothing?

    def search_email_threads(search_str: str):
        #Ask Google API to return threads (or conversations?) that match the search str. Return this to the user more-or-less raw.
        #Note: Need to have good error handling in case there are mistakes in the search_str (would be pretty common)
    

