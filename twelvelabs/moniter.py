##############################################
# Description (AWS Keys are erased + MongoDB password is erased)

# 1. This function get log data from MongoDB and print the following information.
#  - The number of active workers
#  - Total number of videos after searching, filtering and uploading for each query
#  - Average download and upload speed (MB/s) for each worker.
#  - Current video being downloaded by each worker.

##############################################


import pymongo
import pandas as pd

client = pymongo.MongoClient("mongodb+srv://twelvelabs:my_passwords@twelvelabs-cluster.tjtspbg.mongodb.net/")

db = client["mydatabase"]
collection = db["mycollection"]

### 0-1. Get all documents from MongoDB ("Item": "Query_Base")
cursor = collection.find({"Item": "Query_Base"})

workers = []
query_list = []
n_searched_list = []
n_download_list = []
n_upload_list = []
t_download = []

for document in cursor:
    workers.append(document["Worker_Name"])
    query_list.append(document["Query"])
    n_searched_list.append(document["Number of Videos retrieved by Query search"])
    n_download_list.append(document["Number of Videos after filtering"])
    n_upload_list.append(document["Number of Videos Successfully Upload in S3"])
    t_download.append(document["Time_for_Download"])

df_query = pd.DataFrame({
    "Worker": workers,
    "Query": query_list,
    "# of Videos retrieved by Query search": n_searched_list,
    "# of Videos after filtering": n_download_list,
    "# of Videos Successfully Upload in S3": n_upload_list,
    "Time": t_download
})

### 0-2. Get all documents from MongoDB ("Item": "Video_Base")
cursor = collection.find({"Item": "Video_Base"})

videos = []
urls = []
workers = []
sizes = []

for document in cursor:
    videos.append(document["Video_Name"])
    urls.append(document["Video_URL"])
    workers.append(document["Worker_Name"])
    sizes.append(document["Video_size"])

df_video = pd.DataFrame({  
    "Video": videos,
    "URL": urls,
    "Worker": workers,
    "Size": sizes
})


### 1. Number of active workers

worker_names = set()

for worker in workers:
    worker_names.add(worker)

worker_names = list(worker_names)

print("The number of active workers is ", len(worker_names))
# print("The active workers are ", worker_names)

### 2. Total number of videos after searching, filtering and uploading for each query

df_query_without_time = df_query.drop(columns=["Time"])
print(df_query_without_time.T)

### 3. Average download and upload speed (MB/s) for each worker.

for ii in worker_names:
    df_temp1 = df_video[df_video['Worker'] == ii]
    total_size = df_temp1['Size'].sum() / 1024 / 1024      # Byte to MB

    df_temp2 = df_query[df_query['Worker'] == ii]
    total_time = df_temp2['Time'].sum()      # seconds
    
    print(f"Average download and upload speed for {ii} is {total_size/total_time} MB/s")

### 4. Current video being downloaded by each worker.
df_video_without_url_size = df_video.drop(columns=["URL", "Size"])
print(df_video_without_url_size)





