##############################################
# Description (AWS Keys are erased + MongoDB password is erased)

# 1. This function get a video's name and URL, download the video, and upload it to S3 bucket.
# 2. Video will be downloaded and erased from the computer after uploading it to S3 bucket.
# 3. It will be used in main.py

# 4. Print checkpoints to check whether each step is working well.
#  - Checkpoint1 : Download the video from YouTube
#  - Checkpoint2 : Upload the file to S3 bucket
#  - Checkpoint3 : Delete the video file from the computer

# 5. If there are errors (ex. FileNotFoundError, NoCredentialsError), it will print the error message and return False.
    #  - ex. If there is an age restriction, and can't be accessed without logging in, it will return False.

##############################################

import os
import boto3
from pytube import YouTube
from botocore.exceptions import NoCredentialsError

def download_upload(video_name, youtube_url):
    ## Info. about the video
    file_path = f'{video_name}.mp4'
    bucket_name = 'twelvelabs-ytvideo'
    object_name = f'path/in/s3/bucket/{video_name}.mp4'

    ## AWS credentials (Do not share it with anyone) - !!!!!!!!!!!!!!!!!!! I erase my KEYs !!!!!!!!!!!!!!!!!!!
    aws_access_key_id = 'ACCESS_KEY'
    aws_secret_access_key = 'SECRET_KEY'
    
    ## Create an S3 client with credentials
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    try:
        ## Download the video from YouTube
        print("Checkpoint1 : Download the video from YouTube")
        yt = YouTube(youtube_url)
        yt.streams.filter(progressive=True, file_extension='mp4').first().download(filename=f'{video_name}.mp4')

        ## Upload the file to S3 bucket
        print("Checkpoint2 : Upload the file to S3 bucket")
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"File uploaded successfully to {bucket_name}/{object_name}")

        ## Delete the video file from the computer
        print("Checkpoint3 : Delete the video file from the computer")
        os.remove(file_path)
        print(f"Video file '{file_path}' deleted")

        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
