#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 11:06:53 2019

@author: Olukolade Adelabi
This program was made to retreive information from NPR's Public Media Platform
created using a Python PMP SDK https://github.com/KPBS/py3-pmp-wrapper

"""
## IMPORT ##
from pmp_api.pmp_client import Client


## API CREDENTIALS VARIABLES ##
client = Client("https://api.pmp.io")
CLIENT_ID = '4e88e60d-0ffa-493d-bed9-8686e7b2e892'
CLIENT_SECRET = 'e0c46a55c8790cbea20a6917'

## AUTHENTICATE ACCESS ##
client.gain_access(CLIENT_ID, CLIENT_SECRET)

## GET STORY POST ##
print ("Visit https://support.pmp.io/ to gather a GUID")
GUID = input("Please enter the GUID of the post(s) you are looking for: ")

document = client.query('urn:collectiondoc:query:docs', params={"guid": GUID})
collect = document.collectiondoc

## Check for type ##
is_audio = "https://api.pmp.io/profiles/audio"
is_image = "https://api.pmp.io/profiles/image"


## COLLECT MAIN STORY ##
def MainStory(collect, file):
    global title
    global byline
    global description
    global contentencoded
    global teaser
    global tags
    attributes = collect.get('attributes')

    title = ("Title:\n", attributes['title'],"\n")
    file.writelines(title)

    try:
        byline = attributes['byline']
    except KeyError:
        pass
    else:
        byline = ("Byline:\n", attributes['byline'],"\n")
        print("\n")
        file.writelines(byline)

    try:
        teaser = attributes['teaser']
    except KeyError:
        pass
    else:
        teaser = ("Teaser:\n", teaser,"\n")
        print("\n")
        file.writelines(teaser)

    try:
        description = attributes['description']
    except KeyError:
        pass
    else:
        description = ("Media description:\n", description,"\n")

    try:
        contentencoded = attributes['contentencoded']
    except KeyError:
        pass
    else:
        contentencoded = ("Content:\n", contentencoded,"\n")
        print("\n")
        file.writelines(contentencoded)

    try:
       tags = attributes['tags']
    except KeyError:
        pass
    else:
        tags = ("Tags:\n", tags,"\n")
        print("\n")
        file.writelines(tags)

def GetAudio(collect, Items_): # GETS AUDIO
    global audio
    if Items_ == collect.get('items'):
        for item in Items_:
            audio = ("\n Audio link:\n", item['links']['enclosure'][0]['href'],"\n")
    else:
        audio = ("\n Audio link:\n", Items_['enclosure'][0]['href'],"\n")

def GetImage(collect, Items_): #GETS IMAGES
    global john
    global image_set
    image_set = []
    if Items_ == collect.get('items'):
        for item in Items_:
            images = item['links']['enclosure']
    else:
        images = Items_['enclosure']

    for image in images:
        crop = image['meta']['crop']
        href = image['href']
        height = image['meta']['height']
        width = image['meta']['width']
        images = ("Image Links:\n", crop,"-", "Dimensions:", width,'x',height, "\n",href)
        john = " ".join(str(x) for x in images)
        image_set.append(john)

## GET MULTIMEDIA ITEMS ##
def GetItems(collect, is_audio, is_image):
    Items_ = collect.get('items','')
    if Items_ == '':
        Items_ = collect.get('links')
        media_type = Items_['profile'][0]['href']
        if is_audio in media_type:
            GetAudio(collect, Items_)
        elif is_image in media_type:
            GetImage(collect, Items_)
    else:
        for item in Items_:
            media_type = item['links']['profile'][0]['href']
            if is_audio in media_type:
                GetAudio(collect, Items_)
            elif is_image in media_type:
                GetImage(collect, Items_)


## Run Program ##
GetItems(collect, is_audio, is_image)
file = open("NPR.txt", "a")
MainStory(collect, file)
file.writelines(audio)
file.writelines(image_set)
file.close()
