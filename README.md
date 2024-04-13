# WasabiBillingAPI
Sample of API code for accessing Wasabi Billing information

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
```example
xfukaya@kfukaya:~/projects/python/WasabiBillingAPI$ python3 wasabi_billing_get_utilization.py
INFO:__main__:From date = 2024-03-10
INFO:__main__:To date = 2024-03-12
INFO:__main__:Target URL is https://billing.wasabisys.com/utilization
INFO:__main__:status: 200
INFO:__main__:[{'UtilizationNum': 82744145, 'AcctNum': 222373, 'AcctPlanNum': 574816, 'StartTime': '2024-03-10T00:00:00Z', 'EndTime': '2024-03-11T00:00:00Z', 'CreateTime': '2024-03-11T06:56:28Z', 'NumBillableObjects': 27847, 'NumBillableDeletedObjects': 65696, 'RawStorageSizeBytes': 4476074841, 'PaddedStorageSizeBytes': 4477382635, 'MetadataStorageSizeBytes': 3268984, 'DeletedStorageSizeBytes': 89162081234, 'OrphanedStorageSizeBytes': 0, 'MinStorageChargeBytes': 0, 'NumAPICalls': 0, 'UploadBytes': 0, 'DownloadBytes': 0, 'StorageWroteBytes': 0, 'StorageReadBytes': 0, 'NumGETCalls': 0, 'NumPUTCalls': 0, 'NumDELETECalls': 0, 'NumLISTCalls': 0, 'NumHEADCalls': 0, 'DeleteBytes': 0}, {'UtilizationNum': 82831043, 'AcctNum': 222373, 'AcctPlanNum': 574816, 'StartTime': '2024-03-11T00:00:00Z', 'EndTime': '2024-03-12T00:00:00Z', 'CreateTime': '2024-03-12T06:54:56Z', 'NumBillableObjects': 27847, 'NumBillableDeletedObjects': 65696, 'RawStorageSizeBytes': 4476074841, 'PaddedStorageSizeBytes': 4477382635, 'MetadataStorageSizeBytes': 3268984, 'DeletedStorageSizeBytes': 89162081234, 'OrphanedStorageSizeBytes': 0, 'MinStorageChargeBytes': 0, 'NumAPICalls': 13, 'UploadBytes': 19255, 'DownloadBytes': 111277, 'StorageWroteBytes': 0, 'StorageReadBytes': 0, 'NumGETCalls': 0, 'NumPUTCalls': 0, 'NumDELETECalls': 0, 'NumLISTCalls': 0, 'NumHEADCalls': 0, 'DeleteBytes': 0}]
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
INFO:__main__:Utilization Number        : 82831043
INFO:__main__:Account Number            : 222373
INFO:__main__:Account Plan Number       : 574816
INFO:__main__:Start Time                : 2024-03-11T00:00:00Z
INFO:__main__:End Time                  : 2024-03-12T00:00:00Z
INFO:__main__:Create Time               : 2024-03-12T06:54:56Z
INFO:__main__:# of Billable Objects     : 27847
INFO:__main__:# of Billable Deleted objects : 65696
INFO:__main__:Raw Storage Size Bytes        : 4476074841
INFO:__main__:Padded Storage Size Bytes     : 4477382635
INFO:__main__:Metadata Storage Size Bytes   : 3268984
INFO:__main__:Deleted Storage Size Bytes    : 89162081234
INFO:__main__:Orphaned Storage Size Bytes   : 0
INFO:__main__:Minimum Storage Charge Bytes  : 0
INFO:__main__:Number of API Calls           : 13
INFO:__main__:Upload Bytes                  : 19255
INFO:__main__:Download Bytes                : 111277
INFO:__main__:Storage Wrote Bytes           : 0
INFO:__main__:Storage Read Bytes            : 0
INFO:__main__:Number of GET Calls           : 0
INFO:__main__:Number of PUT Calls           : 0
INFO:__main__:Number of DELETE Calls        : 0
INFO:__main__:Number of LIST Calls          : 0
INFO:__main__:Number of HEAD Calls          : 0
INFO:__main__:Delete Bytes                  : 0
xfukaya@kfukaya:~/projects/python/WasabiBillingAPI$
```

## References
## Wasabi Knowledge Base References:
- [How can my Sub-Accounts access Bucket and Utilization data through an API?](https://knowledgebase.wasabi.com/hc/en-us/articles/6890797591323-How-can-my-Sub-Accounts-access-Bucket-and-Utilization-data-through-an-API)
- [Creating a Wasabi API Access Key Set](https://knowledgebase.wasabi.com/hc/en-us/articles/360019677192-Creating-a-Wasabi-API-Access-Key-Set)
- [How do I calculate charges based on bucket utilization?](https://knowledgebase.wasabi.com/hc/en-us/articles/360042869892-How-do-I-calculate-charges-based-on-bucket-utilization)
