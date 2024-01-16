##############################################
# Description (AWS Keys are erased + MongoDB password is erased)

# 1. This function get video's name and return the size of the video file in S3 bucket.
# 2. Since getting video size from 'yt_dlp.YoutubeDL' using 'filesize_approx' parameter is not accurate, 
#    I directly get video size information from S3 bucket.
# 3. It will be used in main.py

# 4. Print original 30 videos lists and filtered videos lists.

##############################################

import boto3

def size_check(video_name):
    # Specify the bucket name
    bucket_name = 'twelvelabs-ytvideo'

    ## AWS credentials (Do not share it with anyone) - !!!!!!!!!!!!!!!!!!! I erase my KEYs !!!!!!!!!!!!!!!!!!!
    aws_access_key_id = 'ACCESS_KEY'
    aws_secret_access_key = 'SECRET_KEY'
        
    ## Create an S3 client with credentials
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # List all objects in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name)

    video_name = "path/in/s3/bucket/" + video_name + ".mp4"

    # Iterate over the objects and filter for videos
    for obj in response['Contents']:
        key = obj['Key']
        
        # Check if the object is a video file and matches the specified video_name
        if (key.endswith('.mp4') or key.endswith('.avi') or key.endswith('.mov')) and key.lower() == video_name.lower():
            try:
                # Get the size of the video file
                response = s3.head_object(Bucket=bucket_name, Key=key)
                size = response['ContentLength']
                
                return size
            except Exception as e:
                print(f"Error: {e}")
                return None
