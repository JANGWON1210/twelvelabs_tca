# Please download and read README.pdf files.

## Detailed Information of the code is in the Python files.
## Additional Information of the code and Results are in the PDF file.


### Task Timeline
23.1.12 ~ 23.1.14 : Due to an environment where code writing is not feasible, the preliminary work began with a focus on internet searches.
  - Investigation into methods for downloading YouTube videos, considering the usage of the YouTube API or relevant packages.
  - Create AWS account for AWS S3 bucket usage and explore on the uploading process in Python.
  - General introductory materials on various database services, exploration of information regarding the strengths and weaknesses of MongoDB and similar services. Preliminary research on the prerequisite knowledge for using MongoDB.

23.1.15 : Wrote Code corresponding to Task 1 + Implementing Example Data Upload Download to MongoDB (About 7 hours)
  - Wrote main.py, get_top_30.py, download_upload.py
  - Adding comments on each files
  + As a first-time user of MongoDB, I uploaded sample data and practiced various features to gain hands-on experience.

23.1.16 : Wrote Code corresponding to Task 2 + Error Correction (About 5 hours, Most of the time was dedicated to error correction.)
  - Wrote size_check.py, moniter.py
  - Adding comments on each files
  - Found error during Multiprocessing process, I fixed the code.
  - After conducting several trials for validation, I identified several errors and subsequently modified the code.
  - Ex) I found an error; if there is an age restriction and access requires logging in, download_upload.py will return False.
  - Consequently, I refined the relevant code and added one more key in the logging process.
  - Ex) I encountered an error during the download and upload of videos to the S3 bucket due to the video name. I refined the code to set a proper name.
  - Moreover, I discovered that a video is not uploaded on AWS if a video with the same name already exists, even if it is not a same video. Therefore, I added some random characters behind the video name.
