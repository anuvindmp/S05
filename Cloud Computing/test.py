import requests
import pprint

url = 'https://llm.biscuitbobby.eu.org/query'
payload = {"message": "search for ma meilleur enemie on youtube.", "max_turns": 2}
response = requests.post(url, json=payload)
pprint.pprint(response.json()['result'])