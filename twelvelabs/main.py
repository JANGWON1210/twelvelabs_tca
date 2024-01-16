##############################################
# Description (AWS Keys are erased + MongoDB password is erased)

# Step 0. Set Worker Name
# Step 1. Get videos names and URLs List.
# Step 1.5. Upload the data to MongoDB
# Step 2. Download and upload videos to S3 bucket.
# Step 3. Record relevant information in MongoDB.

##############################################


from get_top_30 import get_top_30
from download_upload import download_upload
from size_check import size_check
import multiprocessing
import pymongo
import time
import datetime
import socket


if __name__ == "__main__":
    ##############################################
    ### Step 0. Set Worker Name
    ### Worker Name = Hostname + Date : To prevent same worker name, I add date to the worker name.       
    
    worker=socket.gethostname()

    today = datetime.date.today()
    formatted_date = today.strftime("%y%m%d")

    worker+="_"+str(formatted_date)

    ##############################################
    ### Step 1. Get videos names and URLs List.
    ### Detailed information is in get_top_30.py

    query = "baseball highlights"
    name_list, url_list, n_download, n_searched = get_top_30(query)


    ##############################################
    ### Step 1.5. Upload the data to MongoDB
    
    # Connect to MongoDB (!!!!!!!!!!!!!!!!!!!!!! I erase my password !!!!!!!!!!!!!!!!!!!!!)
    client = pymongo.MongoClient("mongodb+srv://twelvelabs:My_Password@twelvelabs-cluster.tjtspbg.mongodb.net/")

    db = client["mydatabase"]
    collection = db["mycollection"]

    group_data = {
        "Item" : "Query_Base",
        "Query": query,
        "Number of Videos after filtering": n_download,
        "Number of Videos retrieved by Query search": n_searched,
        "Worker_Name": worker
    }

    collection.insert_one(group_data)

    for ii in range(len(name_list)):
        group_data = {
            "Item" : "Video_Base",
            "Video_Name": name_list[ii],
            "Video_URL": url_list[ii],
            "Worker_Name": worker
        }
        collection.insert_one(group_data)

   
##############################################
### Step 2. Download and upload videos to S3 bucket. 
### Use multiprocessing to speed up the process.
### Record relevant information in MongoDB.
### Detailed information is in download_upload.py


if __name__ == '__main__':      # to ensure that each individual process only executes the main code block once.
    start =time.time()        # to record the time taken to download and upload videos
    processes = []
    success_count = 0       # to count the number of videos successfully uploaded to S3 bucket

    inputs = [(name, url) for name, url in zip(name_list, url_list)]    

    with multiprocessing.Pool() as pool:
        results = pool.starmap(download_upload, inputs)
    
    # Check the results
    for ii in range(len(results)):
        if results[ii]:
            success_count += 1
        else:
            # in the mongodb, erase the object with the name_list[ii], since it failed to upload to S3 bucket.
            collection.delete_one({"Item" : "Video_Base", "Video_Name": name_list[ii]})
    
    end = time.time()

    print(f"Time taken to download and upload videos is {end-start} seconds")
    print(f"Number of videos successfully uploaded: {success_count}")
    

    ##############################################
    ### Step 3. Record relevant information in MongoDB.
    ### Number of videos successfully uploaded to S3 bucket, time taken to download and upload videos, and video size.
    ### Detailed information is in size_check.py

    ### Record the number of videos successfully uploaded to S3 bucket in MongoDB.
    if collection.find_one({"Item" : "Query_Base", "Query": query, "Worker_Name": worker}):
        collection.update_one({"Item" : "Query_Base", "Query": query, "Worker_Name": worker}, {"$set": {"Number of Videos Successfully Upload in S3": success_count}})
    
    ### Record the time taken to download and upload videos in MongoDB.
    if collection.find_one({"Item" : "Query_Base", "Query": query, "Worker_Name": worker}):
        collection.update_one({"Item" : "Query_Base", "Query": query, "Worker_Name": worker}, {"$set": {"Time_for_Download": end-start}})

    ### Get video size and record it in MongoDB.
    for name in name_list:
        video_size=size_check(name)
        if collection.find_one({"Video_Name": name}):
            collection.update_one({"Video_Name": name}, {"$set": {"Video_size": video_size}})
