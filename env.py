import secret

def save_secret_values_in_env_file(**kwargs):
	API_SECRET_SAVED_FILE = "{}/{}".format(secret.config["API_SECRET_FILE_DIRECTORY"], secret.config["API_SECRET_FILE_NAME"])

	api_uid = kwargs.get("uid")
	api_secret = kwargs.get("secret")
	with open(API_SECRET_SAVED_FILE, "w+") as f:
		f.write(f"PAYLOAD_CLIENT_ID={api_uid}\n")
		f.write(f"PAYLOAD_CLIENT_SECRET={api_secret}\n")