
import requests
import os
import argparse, sys

parser=argparse.ArgumentParser()

parser.add_argument('--auth', help='myCloud Bearer token. example "Bearer Xus2RupGMYjyRtGBk5rj20RxgQ==')
parser.add_argument('--env', help='Enviroment: prod, dev2 or test')

args=parser.parse_args()

username = ''

env = 'dev2'
auth_token = 'Bearer RupSMYjyRtGBk5rj20RxgQ=='


auth_token = 'Bearer lAM6wZROSBWNqJRlyoZmeA=='
env = 'prod'

location = 'downloads' + '/' + env

env_url = 'https://library.'+ env + '.mdl.swisscom.ch'

payload={}
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Authorization': auth_token
    }

    

def download_single_object(image_meta, current_dir):
    base_url = env_url + "/download/"
    
    full_file_path = current_dir + '/' + image_meta['Name']
    
    file_size = str(round(image_meta['Length'] /1024/1024, 2)) + ' MB'
    
    #check if file already exists
    if os.path.exists(full_file_path):
        print('already exsists. Skipping. ' + full_file_path + ', ' + file_size)
        return
    
    
    url = base_url + image_meta['Identifier']
    
    r = requests.request("GET", url, headers=headers, data=payload, stream=True)
    
    if r.status_code == 200:
        with open(full_file_path, 'wb') as f:
            for chunk in r:
                f.write(chunk)
    
    #modified_time_to_creation = image_meta['TimestampEpoch']
    #os.utime(full_file_path,(modified_time_to_creation, modified_time_to_creation ))
            
    print('File saved:' + full_file_path + ', ' + file_size)
    

def init_timeline_overview():

    url = env_url + "/v2/timeline/index?type=monthly"
    print (url)
    
    r = requests.request("GET", url, headers=headers, data=payload)
   
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
    
    current_dir = location + '/' + year + '/' + month
    os.makedirs(current_dir, exist_ok=True)
    
    #get file list

    response = requests.request("GET", url, headers=headers, data=payload)
    images_of_current_month = response.json()

    for image in images_of_current_month:
        download_single_object(image, current_dir)

def get_current_user_name():
    url = 'https://identity.' + env + '.mdl.swisscom.ch/me'
    r = requests.request("GET", url, headers=headers, data=payload)
    
    r_me = r.json()
    username = r_me['UserName']
    return username
    

location = location + '/' + get_current_user_name()

os.makedirs(location, exist_ok=True)

timeline_json = init_timeline_overview()

for group in timeline_json['Groups']:
    download_photos_per_month(group)

