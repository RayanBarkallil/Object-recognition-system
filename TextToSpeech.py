import os

import requests

url = "https://voicerss-text-to-speech.p.rapidapi.com/"
querystring = {"key":"72f22ee2391f439b9b15c7f56d59f0ac"}
sound_path = "static/sounds"
headers = {
    "content-type": "application/x-www-form-urlencoded",
    "X-RapidAPI-Host": "voicerss-text-to-speech.p.rapidapi.com",
    "X-RapidAPI-Key": "ded4dd7a60mshcf8f0adbc7ffb89p164143jsna79cf1cbd63b"
}

def transformString(string): #transform space to %20
    transformation = ""
    for c in string :
        if c == " ":
            transformation += "%20"
        else:
            transformation += c
    return transformation

def setPayload(string):
    source = "src="+string
    parameters = "&hl=en-us&r=0&c=mp3&f=8khz_8bit_mono"
    payload = source+parameters
    return payload

def downloadSoundOf(filename,string):
    payload = setPayload(string)
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    mp3_file = open(sound_path+"/"+filename+".mp3", "wb")
    mp3_file.write(response.content)
    mp3_file.close()

def downloadSoundOf(string):
    payload = setPayload(string)
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    mp3_file = open(sound_path+"/"+string+".mp3", "wb")
    mp3_file.write(response.content)
    mp3_file.close()


def initialiseSounds():
    #get labels :
    classLabels = "beaver, dolphin, otter, seal, whale, aquarium fish, flatfish, ray, shark, trout, orchids, poppies, roses, sunflowers, tulips, bottles, bowls, cans, cups, plates, apples, mushrooms, oranges, pears, sweet peppers, clock, computer keyboard, lamp, telephone, television, bed, chair, couch, table, wardrobe, bee, beetle, butterfly, caterpillar, cockroach, bear, leopard, lion, tiger, wolf, bridge, castle, house, road, skyscraper, cloud, forest, mountain, plain, sea, camel, cattle, chimpanzee, elephant, kangaroo, fox, porcupine, possum, raccoon, skunk, crab, lobster, snail, spider, worm, baby, boy, girl, man, woman, crocodile, dinosaur, lizard, snake, turtle, hamster, mouse, rabbit, shrew, squirrel, maple, oak, palm, pine, willow, bicycle, bus, motorcycle, pickup truck, train, lawn-mower, rocket, streetcar, tank, tractor"
    LABELS = classLabels.split(", ")
    LABELS.sort()
    available_sounds = os.listdir(sound_path)
    for label in LABELS :
        if (label+".mp3") in available_sounds:
            # print("[INFO] skipping ",label+".mp3")
            continue
        downloadSoundOf(label)