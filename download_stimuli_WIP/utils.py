import os, time
from psychopy import core, logging
import yt_dlp
from yt_dlp.utils import download_range_func

def ytdl(url,timestamp,duration,outpath='./'):
    minutes, seconds = timestamp.strip().split(':')

    # Convert minutes and seconds to integers
    minutes = int(minutes)
    seconds = int(seconds)
    
    # Convert minutes to seconds and add to the total seconds
    start = minutes * 60 + seconds
    
    stop = start + duration

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'paths' : {'home':outpath},
        'download_ranges' : download_range_func(None,[(start,stop)]),
        'force_keyframes_at_cuts': True, # for yt links,
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav', #m4a ?
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download([url])

if __name__ == "__main__" :
    tracks_dir = "/home/maellef/git/MuteMusic/data/test"
    for track in os.listdir(tracks_dir):
        track_path = os.path.join(tracks_dir, track)
        print(track_path)



