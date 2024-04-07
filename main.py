import logging
import traceback

from fortytwo_auto_api import fortytwo_auto_keys
import log
import env

fortytwo = fortytwo_auto_keys(
	login=env.config["LOGIN_42"],
	password=env.config["PASSWORD_42"],
	app_url=env.config["APP_URL"],
	otp_secret=env.config["OTP_SECRET_42"],
)

def main():
	try:
		log.setup_logger()
		fortytwo.auto()
		env.save_secret_values_in_env_file(**fortytwo.keys)
		
	except Exception as e:
		logging.error(traceback.format_exc())

if __name__ == "__main__":
	main()