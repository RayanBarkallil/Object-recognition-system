import requests


url = "https://voicerss-text-to-speech.p.rapidapi.com/"

querystring = {"key":"undefined"}

payload = "src=Hello%2C%20world!&hl=en-us&r=0&c=mp3&f=8khz_8bit_mono"
headers = {
    "content-type": "application/x-www-form-urlencoded",
    "X-RapidAPI-Host": "voicerss-text-to-speech.p.rapidapi.com",
    "X-RapidAPI-Key": "SIGN-UP-FOR-KEY"
}

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
print(response.text)


