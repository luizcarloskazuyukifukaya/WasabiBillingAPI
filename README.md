# WasabiBillingAPI
Sample of API code for accessing Wasabi Billing information.
The billing information can be retrieved in two forms, on the account level or per bucket level. The target account is the one with the access key and secret key provided.  
When calling the Billing API, you are required to provide the access key and the secret key for authentication so you get the response successfully. The target account will be the account associated with the access key provided. 

## Quick Start
### Setup
Please refer to the following [document](https://github.com/luizcarloskazuyukifukaya/s3pythonsamples/blob/main/README.md) for the setup of the environment.

### Clone GitHub Repository
Then, you will need to clone this GitHub repository to your local environment, so you can execute the codes.
 Select any folder/directory where you want to clone the samples with the following command:
 
```
git clone https://github.com/luizcarloskazuyukifukaya/WasabiBillingAPI
cd WasabiBillingAPI
```
### Python Code Execution
Now, you are ready to start executing the samples with the following command:
```Python
python <python file>
```
**(Note)** Depending on your environment, "python" command could be different, for example, for Linux it could be "python3".

### JSON OUTPUT
When the csv parameter is not specified or explicitly specified with "false", the output will be with JSON format.

```example JSON
xfukaya@kfukaya:~/projects/python/WasabiBillingAPI$ python3 wasabi_billing_get_utilization.py
INFO:__main__:(option specified) csv = false
INFO:__main__:From date = 2024-03-10
INFO:__main__:To date = 2024-03-11
INFO:__main__:Target URL is https://billing.wasabisys.com/utilization
INFO:__main__:status: 200
INFO:__main__:Utilization Number        : 82744145
INFO:__main__:Account Number            : 222373
INFO:__main__:Account Plan Number       : 574816
INFO:__main__:Start Time                : 2024-03-10T00:00:00Z
INFO:__main__:End Time                  : 2024-03-11T00:00:00Z
INFO:__main__:Create Time               : 2024-03-11T06:56:28Z
INFO:__main__:# of Billable Objects     : 27847
INFO:__main__:# of Billable Deleted objects : 65696
INFO:__main__:Raw Storage Size Bytes        : 4476074841
INFO:__main__:Padded Storage Size Bytes     : 4477382635
INFO:__main__:Metadata Storage Size Bytes   : 3268984
INFO:__main__:Deleted Storage Size Bytes    : 89162081234
INFO:__main__:Orphaned Storage Size Bytes   : 0
INFO:__main__:Minimum Storage Charge Bytes  : 0
INFO:__main__:Number of API Calls           : 0
INFO:__main__:Upload Bytes                  : 0
INFO:__main__:Download Bytes                : 0
INFO:__main__:Storage Wrote Bytes           : 0
INFO:__main__:Storage Read Bytes            : 0
INFO:__main__:Number of GET Calls           : 0
INFO:__main__:Number of PUT Calls           : 0
INFO:__main__:Number of DELETE Calls        : 0
INFO:__main__:Number of LIST Calls          : 0
INFO:__main__:Number of HEAD Calls          : 0
INFO:__main__:Delete Bytes                  : 0
INFO:__main__:-----------------------------------------------------------------------------------
INFO:__main__:Total Storage     : 93642732853
INFO:__main__:Active Storage    : 4480651619
INFO:__main__:deleted Storage   : 89162081234
INFO:__main__:-----------------------------------------------------------------------------------
xfukaya@kfukaya:~/projects/python/WasabiBillingAPI$
```

### CSV OUTPUT
When the csv parameter is specified with "true", the output will be with CSV format.

```example CSV
xfukaya@kfukaya:~/projects/python/WasabiBillingAPI$ python3 wasabi_billing_get_utilization.py
INFO:__main__:(option specified) csv = true
INFO:__main__:From date = 2024-03-04
INFO:__main__:To date = 2024-03-11
INFO:__main__:Target URL is https://billing.wasabisys.com/utilization
INFO:__main__:status: 200
StartTime,EndTime,NumBillableActiveStorageObjects,NumBillableDeletedStorageObjects,RawActiveStorageBytes,BillableActiveStorageBytes,BillableDeletedStorageBytes,NumAPICalls,IngressBytes,EgressBytes
2024-03-04T00:00:00Z,2024-03-05T00:00:00Z,27844,65699,4465589081,4470157171,89162093522,0,0,0
2024-03-05T00:00:00Z,2024-03-06T00:00:00Z,27844,65699,4465589081,4470157171,89162093522,0,0,0
2024-03-06T00:00:00Z,2024-03-07T00:00:00Z,27844,65698,4465589081,4470157171,89162089426,0,0,0
2024-03-07T00:00:00Z,2024-03-08T00:00:00Z,27844,65693,4465589081,4470157171,89162068946,0,0,0
2024-03-08T00:00:00Z,2024-03-09T00:00:00Z,27847,65696,4476074841,4480651619,89162081234,497,361795,665164
2024-03-09T00:00:00Z,2024-03-10T00:00:00Z,27847,65696,4476074841,4480651619,89162081234,0,0,0
2024-03-10T00:00:00Z,2024-03-11T00:00:00Z,27847,65696,4476074841,4480651619,89162081234,0,0,0

xfukaya@kfukaya:~/projects/python/WasabiBillingAPI$
```

## Storage Calculation
The storage values are calculated as shown below:

Total Storage = Active Storage + Deleted Storage  
Active Storage = PaddedStorageSizeBytes + MetadataStorageSizeBytes  
Deleted Storage  = DeletedStorageSizeBytes  

## References
## Wasabi Knowledge Base References:
<!-- - [How can my Sub-Accounts access Bucket and Utilization data through an API?](https://knowledgebase.wasabi.com/hc/en-us/articles/6890797591323-How-can-my-Sub-Accounts-access-Bucket-and-Utilization-data-through-an-API) -->
- [How can my Sub-Accounts access Bucket and Utilization data through an API?](https://docs.wasabi.com/docs/how-can-my-sub-accounts-access-bucket-and-utilization-data-through-an-api)

<!-- - [Creating a Wasabi API Access Key Set](https://knowledgebase.wasabi.com/hc/en-us/articles/360019677192-Creating-a-Wasabi-API-Access-Key-Set) -->
- [Creating a Wasabi API Access Key Set](https://docs.wasabi.com/docs/creating-a-user-account-and-access-key)

<!-- - [How do I calculate charges based on bucket utilization?](https://knowledgebase.wasabi.com/hc/en-us/articles/360042869892-How-do-I-calculate-charges-based-on-bucket-utilization) -->
- [How do I calculate charges based on bucket utilization?](https://docs.wasabi.com/docs/how-do-i-calculate-charges-based-on-bucket-utilization)
