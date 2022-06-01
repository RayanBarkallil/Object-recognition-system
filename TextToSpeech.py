import requests

url = "https://voicerss-text-to-speech.p.rapidapi.com/"

querystring = {"key":"72f22ee2391f439b9b15c7f56d59f0ac"}

payload = "src=Hello%2C%20world!%20I'am%20happy%20to%20say%20that%20this%20is%20working&hl=en-us&r=0&c=mp3&f=8khz_8bit_mono"
headers = {
    "content-type": "application/x-www-form-urlencoded",
    "X-RapidAPI-Host": "voicerss-text-to-speech.p.rapidapi.com",
    "X-RapidAPI-Key": "ded4dd7a60mshcf8f0adbc7ffb89p164143jsna79cf1cbd63b"
}

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

mp3_file = open("label.mp3","wb")
mp3_file.write(response)
mp3_file.close()
print(response.text)