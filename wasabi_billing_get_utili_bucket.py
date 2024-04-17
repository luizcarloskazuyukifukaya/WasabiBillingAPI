# Wasabi Billing API reference
# https://knowledgebase.wasabi.com/hc/en-us/articles/6890797591323-How-can-my-Sub-Accounts-access-Bucket-and-Utilization-data-through-an-API

# GET https://billing.wasabisys.com/utilization/bucket/?withname=true&from=2022-05-31&to=2022-06-01 
# This will give you all the Bucket Utilization metrics including the Bucket Name for May 31 to June 1. This is essentially 1 daily record for each bucket on June 1.

import requests
import logging
import boto3

# Wasabi Billing modules
from wasabi_billing import get_aws_credentials, calculate_storage

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
  withnameFlag = False  # (optional) withname='false'

  logger.debug(f"******* Input parameter =  {params}")

  i = 0
  for key, value in params.items():
    logger.debug(f"---- {key}: {value}")

    # check withname=true flag
    if key == "withname":
      if value == "true":
        withnameFlag = True
        logger.info(f"(option specified) withname = {value}")
      elif value == "false":
        withnameFlag = False
        logger.info(f"(option specified) withname = {value}")
      else:
        logger.info(
            f"(option specified, but the value is wrong. Dismiss it.) withname = {value}"
        )
        # continue

    # check csv=true flag
    elif key == "csv":
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
        # continue
    else:
      # check date format
      try:
        # res = bool(datetime.strptime(value, format))
        if key == "f":
          logger.debug(f"From date = {value}")
          fromDate = value
          paramValidNum = paramValidNum + 1
        if key == "t":
          logger.debug(f"To date = {value}")
          toDate = value
          paramValidNum = paramValidNum + 1

      except ValueError:
        # res = False
        break

      # if paramValidNum == 2:
      #     break

  return paramValidNum, csvFlag, fromDate, toDate, withnameFlag
  # return paramValidNum, True, fromDate, toDate, withnameFlag

# Show information with the CSV Response
def show_CSV_response(r):
    ## Response CSV
    utils = {}

    logger.debug(f"CSV response to be shown ...")

    logger.debug(f"{r}")
    logger.debug(f"{type(r)}")

    logger.debug(f"{r.text}")
    logger.debug(f"{type(r.text)}")

    if r.status_code == 200:
        utils = r.text
        # Show CSV
        print(f"{r.text}")

# Show information with the JSON Response
def show_JSON_response(r):
    ## Response JSON
    utils = {}
    all_total_storage = 0
    all_active_storage = 0
    all_deleted_storage = 0

    logger.debug(f"{r.json()}")
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
        # logger.info(f"Utilization Number        : {util['UtilizationNum']}")
        logger.info(f"Bucket Utilization Number : {util['BucketUtilizationNum']}")
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
        # logger.info(f"Minimum Storage Charge Bytes  : {util['MinStorageChargeBytes']}")
        logger.info(f"Number of API Calls           : {util['NumAPICalls']}")
        logger.info(f"Upload Bytes                  : {util['UploadBytes']}")
        logger.info(f"Download Bytes                : {util['DownloadBytes']}")
        logger.info(f"Storage Wrote Bytes           : {util['StorageWroteBytes']}")
        logger.info(f"Storage Read Bytes            : {util['StorageReadBytes']}")

        logger.info(f"Time to Calculation           : {util['TimeToCalc']}")

        logger.info(f"Number of GET Calls           : {util['NumGETCalls']}")
        logger.info(f"Number of PUT Calls           : {util['NumPUTCalls']}")
        logger.info(f"Number of DELETE Calls        : {util['NumDELETECalls']}")
        logger.info(f"Number of LIST Calls          : {util['NumLISTCalls']}")
        logger.info(f"Number of HEAD Calls          : {util['NumHEADCalls']}")

        logger.info(f"VaultName                     : {util['VaultName']}")

        logger.info(f"Delete Bytes                  : {util['DeleteBytes']}")

        logger.info(f"Bucket                        : {util['Bucket']}")
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
        all_total_storage = all_total_storage + total_storage
        all_active_storage = all_active_storage + active_storage
        all_deleted_storage = all_deleted_storage + deleted_storage

    #ALL TOTAL
    logger.info("###################################################################################")
    logger.info(f"ALL Total Storage     : {all_total_storage}")
    logger.info(f"ALL Active Storage    : {all_active_storage}")
    logger.info(f"ALL deleted Storage   : {all_deleted_storage}")
    logger.info("###################################################################################")
# By using Wasabi Billing Endpoints, your Sub-Accounts can access daily summary utilization of their Sub-Account as well as daily utilizations of all buckets broken down into per-bucket components.

# API Base URL: https://billing.wasabisys.com

# Available Endpoints:
# GET /utilization/bucket
# Parameters to query with
#   from: yyyy-mm-dd #Data from this date
#   to, yyyy-mm-dd #Data to this date
#   csv, true #Format the response in a CSV format
#   withname, true # Includes bucket name in the response

# Authorization Header
#   Authorization: <access_key>:<secret_key>

def get_utilization_bucket(**inputParams):
    ## Utilization Information with bucket
    utils = {}

    logger.debug(f"params [{inputParams}]")

    # number of valid parameters
    paramValidNum = 0
    csvFlag = False  # (optional) csv='true'
    fromDate = ""  # start date 'YY-MM-DD'
    toDate = ""  # end date 'YY-MM-DD'
    withnameFlag = False  # (optional) withname='true'

    paramValidNum, csvFlag, fromDate, toDate, withnameFlag = check_param(**inputParams)
    logger.debug(f"paramValidNum [{paramValidNum}]")
    logger.debug(f"csvFlag [{csvFlag}]")
    logger.debug(f"fromDate [{fromDate}]")
    logger.debug(f"toDate [{toDate}]")
    logger.debug(f"withnameFlag [{withnameFlag}]")

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
        logger.debug(f"HTTP(s) param =  {httpParam}")

    # If optional parameter (csv=true) is specified
    if csvFlag:
        httpParam["csv"] = "true"
    else:
        httpParam["csv"] = "false"
    logger.debug(f"HTTP(s) param =  {httpParam}")

    # If optional parameter (withname=true) is specified
    if withnameFlag:
        httpParam["withname"] = "true"
    else:
        httpParam["withname"] = "false"
    logger.debug(f"HTTP(s) param =  {httpParam}")

    ## API Key value
    access_key, secret_key = get_aws_credentials(AWS_PROFILE)
    logger.debug(f"Access Key is {access_key}")
    logger.debug(f"Secret Key is {secret_key}")

    ## Request Header with API Key Authentication
    #  Authorization: <access_key>:<secret_key>
    auth_value = f"{access_key}:{secret_key}"
    api_head = {"Authorization": auth_value}

    # GET /utilization/bucket/ # NEED TO ADD "/"
    # Example:
    # GET https://billing.wasabisys.com/utilization/bucket/?withname=true&from=2022-05-31&to=2022-06-01
    url = "https://billing.wasabisys.com/utilization/bucket/"
    logger.info(f"Target URL is {url}")

    ## Request
    logger.debug(f"Header: {api_head}")
    logger.debug(f"Body: {httpParam}")

    ## GET request
    ## requests.get(url, params={key: value}, args)
    r = requests.get(url, headers=api_head, params=httpParam)

    ## Response
    logger.debug(f"response: {r}")

    ## Response status code
    logger.info(f"status: {r.status_code}")

    if csvFlag:
        show_CSV_response(r)
    else:
        show_JSON_response(r)
        utils = utils = r.json()

    return utils

# Main function defined here
import sys

def main():

  # # Parameters
  # logger.debug(f"Calling get_utilization_bucket(withname, f, t, csv) ...")
  # all_utils = get_utilization_bucket(withname="true", f="2024-03-11", t="2024-03-12", csv="true")
  # logger.debug(f"get_utilization_bucket(withname, f, t, csv).")
  # ## return value
  # logger.debug(f"{all_utils}")
  # logger.debug(f"{type(all_utils)}")

  # Parameters
  logger.debug(f"Calling get_utilization_bucket(withname, f, t, csv) ...")
  all_utils = get_utilization_bucket(withname="true", f="2024-03-11", t="2024-03-12", csv="false")
  logger.debug(f"get_utilization_bucket(withname, f, t, csv).")
  ## return value
  logger.debug(f"{all_utils}")
  logger.debug(f"{type(all_utils)}")

  # # Parameters
  # logger.debug(f"Calling get_utilization_bucket(withname, f, t) ...")
  # all_utils = get_utilization_bucket(withname="true", f="2024-03-11", t="2024-03-12")
  # logger.debug(f"get_utilization_bucket(withname, f, t).")
  # ## return value
  # logger.debug(f"{all_utils}")
  # logger.debug(f"{type(all_utils)}")

if __name__ == "__main__":
    main()
