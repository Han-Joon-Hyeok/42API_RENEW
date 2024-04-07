from fortytwo_auto_api import fortytwo_auto_keys
import secret

fortytwo = fortytwo_auto_keys(
	login=secret.config["LOGIN_42"],
	password=secret.config["PASSWORD_42"],
	app_url=secret.config["APP_URL"],
	otp_secret=secret.config["OTP_SECRET_42"],
)

fortytwo.auto()

API_SECRET_SAVED_FILE = secret.config["API_SECRET_FILE_PATH"] + secret.config["API_SECRET_FILE_NAME"]

api_keys = fortytwo.keys
with open(API_SECRET_SAVED_FILE, "w+") as f:
	f.write(f"PAYLOAD_CLIENT_ID={api_keys['uid']}\n")
	f.write(f"PAYLOAD_CLIENT_SECRET={api_keys['secret']}\n")
