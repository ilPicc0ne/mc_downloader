import requests
import os
import argparse, sys
from sys import exit
import threading
import threading, queue

import mc_api


env = 'prod'
flat = False

parser=argparse.ArgumentParser()
parser.add_argument('--auth', help='myCloud Bearer token. example "Bearer Xus2RupGMYjyRtGBk5rj20RxgQ==')
#
parser.add_argument('--env', help='Enviroment: prod, dev2 or test')
parser.add_argument('-f', action='store_true', help='Adding this option will download all images without creating sub-folders (year/month)')
args=parser.parse_args()

auth_token = args.auth
if (args.f):
    flat = True


if (args.auth):
    print()
else:
    auth_token = input ("Please paste myCloud authentication token (e.g. Bearer Xus2RupGMYjyRtGBk5rj20RxgQ==): ")


if args.env:
    env = args.env

#initializing default variables
username = ''
location = ''
env_url = 'https://library.'+ env + '.mdl.swisscom.ch'



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
    
        
def download_single_object(image_meta, current_dir):
    base_url = env_url + "/download/"
    
    full_file_path = current_dir + '/' + image_meta['Name']
    
    file_size = str(round(image_meta['Length'] /1024/1024, 2)) + ' MB'
    
    #check if file already exists
    if os.path.exists(full_file_path):
        print('already exsists. Skipping. ' + full_file_path + ', ' + file_size)
        return
    
    
    url = base_url + image_meta['Identifier']
    
    r = request_get_url(url, True)
    
    if r.status_code == 200:
        with open(full_file_path, 'wb') as f:
            for chunk in r:
                f.write(chunk)
    
    #modified_time_to_creation = image_meta['TimestampEpoch']
    #os.utime(full_file_path,(modified_time_to_creation, modified_time_to_creation ))
            
    print('File saved:' + full_file_path + ', ' + file_size)
    

def createNewDownloadThread(image_meta, current_dir):
    download_thread = threading.Thread(target=download_single_object, args=(image_meta,current_dir))
    download_thread.start()
    
    
def init_timeline_overview():

    url = env_url + "/v2/timeline/index?type=monthly"
    
    r = request_get_url(url, False)
   
    timeline_json = r.json()
    print(timeline_json['TotalAssets'])
    return timeline_json
    

def download_photos_per_month(month_group):
    base_url = env_url + "/v2/timeline/monthly/"
    
    year = str(month_group['Year'])
    month = str(month_group['Month'])
    
    year_month =  year + '/' + month
    url = base_url + year_month
    
    print('Starting download for ' + year_month)
    print('Containing ' + str(month_group['Count']) + ' assets')
    
    #creating directory for current month
    current_dir = location 
    if flat == False:
        current_dir = current_dir + '/' + year + '/' + month
    
    os.makedirs(current_dir, exist_ok=True)
    
    #get file list

    r = request_get_url(url, False)
    images_of_current_month = r.json()

    for image in images_of_current_month:
        createNewDownloadThread(image, current_dir)
        #download_single_object(image, current_dir)

def get_current_user_name():
    url = 'https://identity.' + env + '.mdl.swisscom.ch/me'
    r = request_get_url(url, False)
    
    r_me = r.json()
    username = r_me['UserName']
    return username




if location == '':
    location = get_current_user_name()
else:
    location = location + '/' + get_current_user_name()

timeline_json = init_timeline_overview()

os.makedirs(location, exist_ok=True)

for group in timeline_json['Groups']:
    download_photos_per_month(group)
    
    
    
