import requests


def request_get_url(url, stream_on):
    payload={}
    headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Authorization': auth_token
    }
    
    r = requests.request("GET", url, headers=headers, data=payload, stream=stream_on)
    
    try: 
        if r.status_code == 401:
            print('The auhtoriation token you provided is invalid for the Chosen environment ' + env)
            input('Please restart with valid bearer. Press any key to quit.')
            exit(0)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e: 
        print (e)
    
    return r