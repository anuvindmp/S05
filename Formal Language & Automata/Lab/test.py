import requests
import pprint

url = 'https://llm.biscuitbobby.eu.org/query'
payload = {"message": "take a picture and tell me what is in front of it via discord", "max_turns": 2}
response = requests.post(url, json=payload)
pprint.pprint(response.json()['result'])