# Python Code to interact with Gmail via Google API
This repo is for a challenge undertaken as a test for a Data Engineering position, originally found at this link: https://github.com/haensel-ams/recruitment_challenge/tree/master/DevOps_201909.

The instructions below show you how to use this repo more - if you have any questions or concerns, please raise an issue on this repo and the author will get back to you soon!

---

## What does this code do?
This code allows you to interact with Gmail just from using a Python script without having to use Gmail from your web browser. Exciting!

Currently this code only supports the following functionalities, but more may be added in the future:
- Compose & send emails
- Search through your Gmail inbox to find specific messages

---

## How can I use this code?

### Step 1: Setting up your Google Cloud Project
Using the Google API means that you need your own Google Cloud Project.
This is what allows Google to expose access to parts of your Google account to APIs - and helps you manage authentication.
You can follow [Google's instructions to set up a Google Cloud Project](https://developers.google.com/workspace/guides/create-project).

---

### Step 2: Enable the Gmail API on your Project
1. Follow [Google's instructions to enable Google Workspace APIs](https://developers.google.com/workspace/guides/enable-apis) to locate where you can activate the Gmail API
2. Once you see the page below, click the 'Gmail API' and then click 'Enable' <br><img src="./media/google-api-library.png" alt="Google API product library" width = 600px;>

---

### Step 3: Setting up OAuth authentication
Google offers a few ways to authenticate API calls, but for using Gmail specifically without a Google Workspace account, OAuth is the best choice (see `devnotes.md` for a discussion of this topic).
1. In your Project, find the "Credentials" menu within "APIs & Services"<br><img src="./media/api-credentials-menu.png" alt="API Credentials menu" width = 300px;>
2. Click 'Create Credentials' at the top menu and then select "OAuth client ID"
3. Select the application type "Desktop app" and then click "Create"
4. The OAuth client will be created and a pop-up will offer you a chance to download the credentials as a JSON file. Do this and move this file to a secure location on your computer.
5. *[optional]* Rename this file to "credentials.json" for easier use.

---

### Step 4: Setting up this code on your computer
1. [Download and install Python](https://www.python.org/downloads/) if you haven't already
2. Clone this Github repository using Git, or download it as a zip file and unpack it in a folder on your computer.
3. Run the code snippets below to set up your environment. Note that these code snippets are for **Linux**. To see how to set up a virtual environment on Windows or Mac machines, see the [Python documentation on virtual environments](https://docs.python.org/3/library/venv.html)


```
Setup a Python virtual environment in a folder 'venv' alongside your code:
>$ python3 -m venv path/to/your/folder/venv
```
```
Activate your Python virtual environment:
>$ source venv/bin/activate
```
```
Install dependent packages
(venv)>$ pip install -r requirements.txt
```

### Step 3: Running this code:
If you've completed all of the commands above, you should be ready to go!
See the 'quickstart.py' script for some examples of how you can use this code. You will need to change a few things (particularly where you are storing your OAuth credentials) for the code to run correctly.


### Step 4: Exiting your virtual environment:
Once you're done using the code, you can exit the environment by using the command below:
```
(venv)>$ deactivate
```

---

