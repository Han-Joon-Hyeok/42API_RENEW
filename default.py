#!/usr/bin/env python3
"""Sample code
Get API Keys and write this to an env file
"""

from fortytwo_auto_api import fortytwo_auto_keys
import secret

fortytwo = fortytwo_auto_keys(
	login=secret.LOGIN_42,
	password=secret.PASSWORD_42,
	app_url=secret.APP_URL,
	otp_secret=secret.OTPSECRET_42,
)

fortytwo.auto()

api_keys = fortytwo.keys
with open(".env.api", "w+") as f:
	f.write(f"PAYLOAD_CLIENT_ID={api_keys['uid']}\n")
	f.write(f"PAYLOAD_CLIENT_SECRET={api_keys['secret']}\n")
