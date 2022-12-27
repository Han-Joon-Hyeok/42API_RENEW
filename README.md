# Get your 42 API creds automaticly

## Requierements
You need a browser (Chrome/Firefox) and its associated driver.
This two executable need to be in PATH.

Chrome example:
```
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dkpg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install
mkdir -p /opt/web_drivers; cd /opt/web_drivers/; wget https://chromedriver.storage.googleapis.com/107.0.5304.18/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
```
And add /opt/web_drivers to your path. If you have any problems, please refer to selenium docs : https://selenium-python.readthedocs.io/installation.html

After that :
```
python3 -m pip install -r requirements.txt
```

## Usage
You will need to create a file named `secret.py` containing :
```python
LOGIN_42="<42_login>"
PASSWORD_42="<42_password>"
OTPSECRET_42="<OTP_secret>" # Or None
APP_URL="https://profile.intra.42.fr/oauth/applications/<app_id>"
```

The class with all operations is in `fortytwo_auto_api`. You will find a `default.py` containing an example.

## Problems
- Take care of the `secret.py` file, configure ACL correctly
- Can't test with Firefox because i'm on Windows and WSL (sorry 😒)
- If 42 change its HTML code, it will certainly break i will try to update it

