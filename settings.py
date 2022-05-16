from configparser import ConfigParser

config = ConfigParser()
config.read("cred_file.ini")

aws_access_key = config.get("DEFAULT", "aws_access_key")
aws_secret_key = config.get("DEFAULT", "aws_secret_key")
region = config.get("DEFAULT", "region")
bucket_name = config.get("DEFAULT", "bucket_name")
folder_name = config.get("DEFAULT", "folder_name")
kafka_topic = config.get("DEFAULT", "kafka_topic")
