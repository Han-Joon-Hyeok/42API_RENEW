import logging
import traceback

from src.fortytwo_auto_api import fortytwo_auto_keys
from src.log import setup_logger
from src.env import config as env
from src.env import save_secret_values_in_env_file
from src.github_issue import create_issue

fortytwo = fortytwo_auto_keys(
	login=env["LOGIN_42"],
	password=env["PASSWORD_42"],
	app_url=env["APP_URL"],
	otp_secret=env["OTP_SECRET_42"],
)

def main():
	try:
		setup_logger()
		fortytwo.auto()
		save_secret_values_in_env_file(**fortytwo.keys)
		
	except Exception as e:
		logging.error(traceback.format_exc())
		create_issue(traceback.format_exc())

if __name__ == "__main__":
	main()