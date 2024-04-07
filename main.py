import logging
import traceback

from fortytwo_auto_api import fortytwo_auto_keys
import secret
import log
import env

fortytwo = fortytwo_auto_keys(
	login=secret.config["LOGIN_42"],
	password=secret.config["PASSWORD_42"],
	app_url=secret.config["APP_URL"],
	otp_secret=secret.config["OTP_SECRET_42"],
)

def main():
	try:
		log.setup_logger()
		fortytwo.auto()
		env.save_secret_values_in_env_file()
		
	except Exception as e:
		logging.error(e)
		logging.error(traceback.format_exc())

if __name__ == "__main__":
	main()