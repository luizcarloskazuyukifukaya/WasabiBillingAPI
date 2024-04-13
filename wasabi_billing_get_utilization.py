# Wasabi Billing API reference
# https://knowledgebase.wasabi.com/hc/en-us/articles/6890797591323-How-can-my-Sub-Accounts-access-Bucket-and-Utilization-data-through-an-API

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

# Check input parameters
from datetime import datetime

# paramValidNum, csvFlag, fromDate, toDate = check_param(**inputParams)
def check_param(**params):
    # initializing format
    format = "%Y-%m-%d"

    paramValidNum = 0
    csvFlag = False  # (optional) csv='true'
    fromDate = ""  # start date 'YY-MM-DD'
    toDate = ""  # end date 'YY-MM-DD'

    logger.debug(f"Input parameter =  {params}")

    for key, value in params.items():
        logger.debug(f"{key}: {value}")

        # check csv=true flag
        if key == "csv":
            if value == "true":
                csvFlag = True
                logger.info(f"(option specified) csv = {value}")
            elif value == "false":
                csvFlag = False
                logger.info(f"(option specified) csv = {value}")
            else:
                logger.info(
                    f"(option specified, but the value is wrong. Dismiss it.) csv = {value}"
                )
                continue

        # check date format
        try:
            res = bool(datetime.strptime(value, format))
            if key == "f":
                logger.debug(f"From date = {value}")
                fromDate = value
                paramValidNum = paramValidNum + 1
            if key == "t":
                logger.debug(f"To date = {value}")
                toDate = value
                paramValidNum = paramValidNum + 1

        except ValueError:
            res = False
            break

        if paramValidNum == 2:
            break

    return paramValidNum, csvFlag, fromDate, toDate


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


# By using Wasabi Billing Endpoints, your Sub-Accounts can access daily summary utilization of their Sub-Account as well as daily utilizations of all buckets broken down into per-bucket components.

# API Base URL: https://billing.wasabisys.com

# Available Endpoints:
# GET /utilization
# GET /utilization/bucket
# Parameters to query with
#   from: yyyy-mm-dd #Data from this date
#   to, yyyy-mm-dd #Data to this date
#   csv, true #Format the response in a CSV format
# Authorization Header
#   Authorization: <access_key>:<secret_key>

def get_utilization(**inputParams):
    ## Utilization Information
    utils = {}

    # number of valid parameters
    paramValidNum = 0
    csvFlag = False  # (optional) csv='true'
    fromDate = ""  # start date 'YY-MM-DD'
    toDate = ""  # end date 'YY-MM-DD'

    paramValidNum, csvFlag, fromDate, toDate = check_param(**inputParams)
    logger.debug(f"paramValidNum [{paramValidNum}]")
    logger.debug(f"csvFlag [{csvFlag}]")
    logger.debug(f"fromDate [{fromDate}]")
    logger.debug(f"toDate [{toDate}]")

    # If date is not specified, should return {}
    if len(fromDate) == 0:
        return utils
    if len(toDate) == 0:
        return utils

    # From here either param is 2 or 0 and is valid
    # fromDate, toDate to be used when paramValidNum == 2
    # The sub-account AcctNum is specified with 'id'
    # When csvFlag is True, then the most recent calculated utilization is returned
    httpParam = {}
    if paramValidNum == 2:
        logger.debug(f"Input parameter is valid")
        logger.info(f"From date = {fromDate}")
        logger.info(f"To date = {toDate}")

        httpParam["from"] = fromDate
        httpParam["to"] = toDate
        logger.debug(f"HTTP(s) param =  {httpParam}")
    elif paramValidNum == 0:
        logger.debug(f"No input parameter given.")
    else:
        logger.error(f"Input parameter is wrong")
        return utils  # {} NULL

    # If optional parameter (csv=true) is specified
    if csvFlag:
        httpParam["csv"] = "true"

    ## API Key value
    access_key, secret_key = get_aws_credentials(AWS_PROFILE)
    logger.debug(f"Access Key is {access_key}")
    logger.debug(f"Secret Key is {secret_key}")

    ## Request Header with API Key Authentication
    #  Authorization: <access_key>:<secret_key>
    auth_value = f"{access_key}:{secret_key}"
    api_head = {"Authorization": auth_value}

    # GET /utilization
    url = "https://billing.wasabisys.com/utilization"
    logger.info(f"Target URL is {url}")

    ## GET request
    ## requests.get(url, params={key: value}, args)
    r = requests.get(url, headers=api_head, params=httpParam)

    ## Response status code
    logger.info(f"status: {r.status_code}")

    ## Response JSON
    logger.info(f"{r.json()}")
    logger.debug(f"{type(r.json())}")

    if r.status_code == 200:
        utils = r.json()
    for util in utils:
        logger.debug(
            "==================================================================================="
        )
        logger.debug(util)
        logger.debug(
            "-----------------------------------------------------------------------------------"
        )
        logger.info(f"Utilization Number        : {util['UtilizationNum']}")
        logger.info(f"Account Number            : {util['AcctNum']}")
        logger.info(f"Account Plan Number       : {util['AcctPlanNum']}")
        logger.info(f"Start Time                : {util['StartTime']}")
        logger.info(f"End Time                  : {util['EndTime']}")
        logger.info(f"Create Time               : {util['CreateTime']}")
        logger.info(f"# of Billable Objects     : {util['NumBillableObjects']}")
        logger.info(f"# of Billable Deleted objects : {util['NumBillableDeletedObjects']}")
        logger.info(f"Raw Storage Size Bytes        : {util['RawStorageSizeBytes']}")
        logger.info(f"Padded Storage Size Bytes     : {util['PaddedStorageSizeBytes']}")
        logger.info(f"Metadata Storage Size Bytes   : {util['MetadataStorageSizeBytes']}")
        logger.info(f"Deleted Storage Size Bytes    : {util['DeletedStorageSizeBytes']}")
        logger.info(f"Orphaned Storage Size Bytes   : {util['OrphanedStorageSizeBytes']}")
        logger.info(f"Minimum Storage Charge Bytes  : {util['MinStorageChargeBytes']}")
        logger.info(f"Number of API Calls           : {util['NumAPICalls']}")
        logger.info(f"Upload Bytes                  : {util['UploadBytes']}")
        logger.info(f"Download Bytes                : {util['DownloadBytes']}")
        logger.info(f"Storage Wrote Bytes           : {util['StorageWroteBytes']}")
        logger.info(f"Storage Read Bytes            : {util['StorageReadBytes']}")
        logger.info(f"Number of GET Calls           : {util['NumGETCalls']}")
        logger.info(f"Number of PUT Calls           : {util['NumPUTCalls']}")
        logger.info(f"Number of DELETE Calls        : {util['NumDELETECalls']}")
        logger.info(f"Number of LIST Calls          : {util['NumLISTCalls']}")
        logger.info(f"Number of HEAD Calls          : {util['NumHEADCalls']}")
        logger.info(f"Delete Bytes                  : {util['DeleteBytes']}")
        logger.info(
            "-----------------------------------------------------------------------------------"
        )

        # calculate total, active and deleted storage (per day)        
        total_storage, active_storage, deleted_storage = calculate_storage(util)
        logger.info(f"Total Storage     : {total_storage}")
        logger.info(f"Active Storage    : {active_storage}")
        logger.info(f"deleted Storage   : {deleted_storage}")
        logger.info(
            "-----------------------------------------------------------------------------------"
        )


    return utils

# Main function defined here
import sys

def main():
# # for the execution of this script only
# #################################################################
# # case 1: with parameter (f and t)
# logger.debug(f"Calling get_utilization(f, t) ...")
# all_utils = get_utilization(f="2023-11-03", t="2023-11-09")
# logger.debug(f"get_utilization(f,t).")
# ## return value
# logger.info(f"{all_utils}")
# logger.debug(f"{type(all_utils)}")
# #################################################################
# # case 2: with parameter (f only) [Should Fail]
# logger.debug(f"Calling get_util_control_subaccounts(id, f) ...")
# all_utils = get_utilization(f="2023-11-03")
# logger.debug(f"get_util_control_subaccounts(id, f).")
# ## return value
# logger.info(f"{all_utils}")
# logger.debug(f"{type(all_utils)}")
# #################################################################
# # case 3: with parameter (csv='true') [Should Fail, date should be specified]
# logger.debug(f"Calling get_utilization(csv) ...")
# all_utils = get_utilization(csv="true")
# logger.debug(f"get_utilization(csv).")
# ## return value
# logger.info(f"{all_utils}")
# logger.debug(f"{type(all_utils)}")
# #################################################################
# # case 4: with parameter (f and t and csv='true')
# logger.debug(f"Calling get_utilization(f, t, csv) ...")
# all_utils = get_utilization(f="2023-11-03", t="2023-11-09", csv="true")
# logger.debug(f"get_utilization(f, t, csv).")
# ## return value
# logger.info(f"{all_utils}")
# logger.debug(f"{type(all_utils)}")

    # Parameters
    logger.debug(f"Calling get_utilization(f, t, csv) ...")
    all_utils = get_utilization(f="2024-03-10", t="2024-03-11", csv="true")
    logger.debug(f"get_utilization(f, t, csv).")
    ## return value
    logger.debug(f"{all_utils}")
    logger.debug(f"{type(all_utils)}")

    # # Parameters
    # logger.debug(f"Calling get_utilization(f, t) ...")
    # all_utils = get_utilization(f="2024-03-10", t="2024-03-12")
    # logger.debug(f"get_utilization(f, t).")
    # ## return value
    # logger.debug(f"{all_utils}")
    # logger.debug(f"{type(all_utils)}")

    # # THIS SHOULD RETURN NULL AS THE DATES ARE NOT SPECIFIED
    # # Parameters
    # logger.debug(f"Calling get_utilization(csv) ...")
    # all_utils = get_utilization(csv="true")
    # logger.debug(f"get_utilization(csv).")
    # ## return value
    # logger.debug(f"{all_utils}")
    # logger.debug(f"{type(all_utils)}")


if __name__ == "__main__":
    main()
