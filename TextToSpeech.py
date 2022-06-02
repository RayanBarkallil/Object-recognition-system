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

def getSoundOf(filename,string):
    payload = setPayload(string)
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    mp3_file = open(sound_path+"/"+filename+".mp3", "wb")
    mp3_file.write(response.content)
    mp3_file.close()