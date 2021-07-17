import re
from time import sleep

# Progress Bars
from tqdm import tqdm

# Youtube API
from pytube import Playlist
from pytube import YouTube

from utilities import *

# import mutagen # Posible metadata editing in the future

def main():
    # Input
    DOWNLOAD_DIR = 'D:\\Music\\Tests'
    playlist = "https://music.youtube.com/playlist?list=OLAK5uy_mn9NjUilMFKR7ydZ12VxUTga47VKH-0So"

    download_audio(playlist, DOWNLOAD_DIR)


def download_audio(url:str, dir:str):
    # Fetch all videos to download
    videos = get_videos(url)

    print("\n")  # Pretty formating
    for v in tqdm(videos):
        try:
            # 140 is the identifying tag that gets just audio
            # the possible values are in p[n].streams.all()
            audioStream = v.streams.get_by_itag('140')
            
            # Process the title
            filename = filename_processor(v)
            print("\n" + filename)

            # Download
            audioStream.download(output_path=dir, filename=filename)
        except Exception as e:
            print("Error on download")
            print(e)
            sleep(5)
            delete_last_lines()
    
        delete_last_lines(2)  # Pretty formating
        

def filename_processor(v:YouTube) -> str:
    # Remove things inside parenthesis
    title = re.sub(r'\([^)]*\)', '', v.title)
    author = re.sub(r'\([^)]*\)', '', v.author)

    # Remove brackets
    title = re.sub(r'\[[^)]*\]', '', title)

    # Remove this (Case insensitive)
    title = re.sub('music video', '', title, flags=re.IGNORECASE)
    title = re.sub(r'official', '', title, flags=re.IGNORECASE)
    # title = re.sub(r'TVアニメ', '', title, flags=re.IGNORECASE)

    author = re.sub(r'official', '', author, flags=re.IGNORECASE)
    
    # Remove VEVO from author
    author = re.sub("VEVO", "", author)
    # Work in progress fix case sensitivity

    author_in_title: bool = len(re.findall(
        author, title, flags=re.IGNORECASE)) >= 1
    if author_in_title:  # Remove the author's name from the title
        title = re.sub(author, "", title, flags=re.IGNORECASE)

    # Remove extra whitespace
    title = re.sub(r' +', ' ', title)

    # Remove spaces around and stich
    result = f"{title.strip()} - {author.strip()} - {v.video_id}"
    # Remove the topic tag, I still don't know what it means
    result = re.sub(" - Topic", "", result)
    return result


def get_videos(url):
    """Returns a list of YouTube Objects"""
    result = []
    if 'list' in url:
        print("Adding a Playlist")
        playlist = Playlist(url)
        # this fixes the empty playlist.videos list
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        try:
            for i, v in enumerate(playlist.videos):
                # print(f"{i+1}: '{v.video_id}'", end=", ")
                result.append(v)
        except:
            print("Failed creating a list of video urls")
    else:
        result.append(YouTube(url))
    
    return result


if __name__ == "__main__":
    main()
