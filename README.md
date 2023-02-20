# Get your 42 API creds automaticly

## Requierements
You need a browser (Chrome/Firefox) and its associated driver.
This two executable need to be in PATH.

Chrome example:
```
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt-get update 
sudo apt-get install dpkg
sudo apt-get install -y fonts-liberation libasound2 libgbm1 libu2f-udev libvulkan1
sudo apt --fix-broken install
sudo /usr/bin/dpkg -i google-chrome-stable_current_amd64.deb
sudo mkdir -p /opt/web_drivers; sudo cd /opt/web_drivers/; sudo wget https://chromedriver.storage.googleapis.com/110.0.5481.77/chromedriver_linux64.zip
sudo apt install unzip
unzip chromedriver_linux64.zip
```
And add /opt/web_drivers to your path. If you have any problems, please refer to selenium docs : https://selenium-python.readthedocs.io/installation.html

After that :
```
sudo apt-get update
sudo apt-get install -y python3-pip
pip install webdriver_manager
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

