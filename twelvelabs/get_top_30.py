##############################################
# Description

# 1. This function get query(string) return lists of videos' name and URL, number of videos after filtering, and number of videos retrieved by query search
# 2. Top 30 videos will be searched and vidoes which do not meet the condition will be filtered out.
# 3. It will be used in main.py

# 4. Print original 30 videos lists and filtered videos lists.

##############################################

import re
import yt_dlp
import pandas as pd
import random
import string

def get_top_30(query): 
    ydl_opts = {
        'format': 'bestvideo[ext=mp4][height>=720]+bestaudio[ext=m4a]/bestvideo+bestaudio',
        'noplaylist': True,
        'quiet': True,
    }

    ### Search top 30 videos
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info("ytsearch30:" + query, download=False)
        entries = info_dict.get('entries', None)

        if not entries:
            print('No videos found')
            return []
        
        names = []      # Video name(String)
        urls = []    # Video URL(String)
        v_durations = []    # Video duration in seconds
        exts = []       # Video filename extension(ex. mp4)
        heights = []    # Video resoultion-height (ex. 720)
        audios = []     # Video has audio or not
        for entry in entries:
            if len(urls) >= 30:
                print("break")
                break
            
            ### To prevent potential errors, I replace some characters with proper characters.
            entry['title'] = entry['title'].replace('#', '')
            entry['title'] = entry['title'].replace('?', '')
            entry['title'] = entry['title'].replace('!', '')
            entry['title'] = entry['title'].replace(' ', '_')
            entry['title'] = re.sub(r'[^\w]', '', entry['title'])
            
            ### To prevent same video name, I add random string to the video name.
            random_string = ''.join(random.choices(string.ascii_lowercase, k=3))
            entry['title'] = entry['title'] + "_" + random_string

            names.append(entry['title'])
            urls.append(entry['webpage_url'])
            v_durations.append(entry['duration'])
            exts.append(entry['ext'])
            heights.append(entry['height'])
            audios.append(entry['acodec'] != 'none')

            
        df = pd.DataFrame({'Name': names, 'URL': urls, 'Duration': v_durations, 'Resolution': heights, 'Extension': exts, 'Audio': audios})
        
        print("Top 30 videos are selected.")
        print(df)

        ### Filtering videos which do not meet the condition.
        ### 8min~12min, 720p, mp4, audio filter
        df = df[
        (df['Duration'] <= 720) &
        (df['Duration'] >= 480) &
        (df['Resolution'] >= 720) &
        (df['Extension'] == 'mp4') &
        (df['Audio'])
        ]
        
        print(f"{len(df)}/{len(urls)} videos meet constraints.")
        print(df)
        
        return df['Name'].tolist(), df['URL'].tolist(), len(df), len(urls)