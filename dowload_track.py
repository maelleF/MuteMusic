import os 
from utils import ytdl

track_list = [
            {
            'url':'https://www.youtube.com/watch?v=ieU4Am0t0tc',
            'timestamp':'00:00',
            'duration':65
            },
            {
            'url':'https://www.youtube.com/watch?v=RIjTq_OdFvo',
            'timestamp':'00:00',
            'duration':87
            },
            {
            'url':'https://www.youtube.com/watch?v=h55ROrO3UHc',
            'timestamp':'00:00',
            'duration':52
            },
            {
            'url':'https://www.youtube.com/watch?v=0T-if-Vj2Xs',
            'timestamp':'00:00',
            'duration':61
            },
            {
            'url':'https://www.youtube.com/watch?v=iy3qq7zc4EY',
            'timestamp':'00:00',
            'duration':88
            },
            {
            'url':'https://www.youtube.com/watch?v=1rwAvUvvQzQ',
            'timestamp':'01:48',
            'duration':81
            },
            ]

for track in track_list :
    ytdl(track['url'],timestamp=track['timestamp'],duration=track['duration'],outpath='./data/test')

