import logging

import secret

from dotenv import dotenv_values

config = dotenv_values(".env")

def save_secret_values_in_env_file(**kwargs):
	API_SECRET_SAVED_FILE = "{}/{}".format(env.config["API_SECRET_FILE_DIRECTORY"], env.config["API_SECRET_FILE_NAME"])

	api_uid = kwargs.get("uid")
	api_secret = kwargs.get("secret")
	with open(API_SECRET_SAVED_FILE, "w+") as f:
		f.write(f"PAYLOAD_CLIENT_ID={api_uid}\n")
		f.write(f"PAYLOAD_CLIENT_SECRET={api_secret}\n")

	logging.info(f"Successfully API secret saved in {API_SECRET_SAVED_FILE}")