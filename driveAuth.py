from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import time

gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
    print('Refreshed Token')
else:
    # Initialize the saved creds
    gauth.Authorize()
    print('Google Authorized')
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")
drive = GoogleDrive(gauth)


time.sleep(2)
