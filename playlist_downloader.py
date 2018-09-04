#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 12:16:50 2018

@author: krishna
"""


import urllib2
import pytube
import os
import multiprocessing

####### User inputs
download_folder='download_folder'
playlist_url = 'https://www.youtube.com/playlist?list=PL9Lr0N2rRTOTySwboXu_t9tzThBrDpkUO'
###########

if not os.path.exists(download_folder):
    os.mkdir(download_folder)

def extract_links(playlist_url):
    open_link = urllib2.urlopen(playlist_url)
    read_data = open_link.readlines()
    store_data=[]
    for line in read_data:
        if 'pl-video-title-link' in line:
            store_data.append(line)
            
    partial_urls=[]
    for videos in store_data:
        partial_urls.append(videos.split('href="',1)[1].split('" ',1)[0])
    full_urls=[]
    for part_url in partial_urls:
        full_urls.append('http://www.youtube.com'+part_url)
    return full_urls


download_links=extract_links(playlist_url)
print('We found ---->'+str(len(download_links))+' links in the playlist')
print('Downloding....')



def download_videos(url):
    yt=pytube.YouTube(url)
    video =  yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    try:
        video.download(download_folder)
        print('Donwloaded---'+url+'---:):):)')
    except:
        print('could not download the file--->'+url)
        

#### You can change the number of processes if you want
pool = multiprocessing.Pool(processes=32) 
pool.map(download_videos, download_links)    