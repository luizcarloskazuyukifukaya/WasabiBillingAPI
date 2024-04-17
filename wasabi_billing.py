# Wasabi Billing API reference
# https://knowledgebase.wasabi.com/hc/en-us/articles/6890797591323-How-can-my-Sub-Accounts-access-Bucket-and-Utilization-data-through-an-API

# This is a toolbox module for Wasabi billing

import requests
import logging
import boto3

# Create logger object
logging.basicConfig()  # This is important
logger = logging.getLogger(__name__)

# Set logging level (default is WARNING)
# DEBUG    - 10
# INFO     - 20
# WARNING  - 30
# ERROR    - 40
# CRITICAL - 50
LOG_LEVEL = 20
# LOG_LEVEL = 10

# logger samples
# logger.info("This is a info log.")
# logger.warning("This is a warning log.")

# Set logging level
logger.setLevel(LOG_LEVEL) # DEBUG
level = logger.level
logger.debug(f"Current Logging Level is {level}")

# Set logging level
logger.setLevel(LOG_LEVEL)
level = logger.level
logger.debug(f"Current Logging Level is {level}")

from os.path import expanduser
home = expanduser("~")

# return value when the input is not valid
INVALID_KEY = 'no_key'
INVALID_VALUE = ''

# profile to be used
AWS_PROFILE = "wasabi"
# AWS_PROFILE = "default"

# Get AWS access key and secret key from AWS ~/.aws/credential
# This is the method used in AWS CLI and AWS SDK
# Input: profile - profile to be used
# Return: AWS Access key and AWS Secret key
def get_aws_credentials(profile: str):    
    session = boto3.Session(profile_name=profile)
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key

    #print(aws_access_key_id)
    #print(aws_secret_access_key)
    return aws_access_key_id, aws_secret_access_key

# Calculate Storages in bytes got in day only
# Total Storage (TB) = Active Storage (TB) + Deleted Storage (TB)
# Active Storage (TB) = (PaddedStorageSizeBytes + MetadataStorageSizeBytes) / 1024 / 1024 / 1024 / 1024
# Deleted Storage (TB) = DeletedStorageSizeBytes / 1024 / 1024 / 1024 / 1024
def calculate_storage(util):
    deleted = util["DeletedStorageSizeBytes"]
    padded = util['PaddedStorageSizeBytes']
    metadata = util['MetadataStorageSizeBytes']

    deleted_storage = 0
    active_storage = 0
    total_storage = 0

    deleted_storage = int(deleted)
    active_storage = int(padded) + int(metadata)
    total_storage = active_storage + deleted_storage

    return total_storage, active_storage, deleted_storage
