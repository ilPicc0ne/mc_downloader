import requests
import os
import argparse, sys
from sys import exit

from datetime import datetime
from download_manager import DownloadManager, DownloadItem
import helper



env = 'prod'
flat = False
username = ''
location = ''
mc_library_url = ''
mc_identiy_url = ''
auth_token = ''
auth_ok = False

dm = None


def authenticate():
    global auth_token
    while (is_authenticated()== False):
        auth_token = input ("Please paste myCloud authentication token (e.g. Bearer Xus2RupGMYjyRtGBk5rj20RxgQ==): ")
         
def is_authenticated():
    #r = requests.request("GET", mc_identiy_url+'/me', headers=headers, data=payload)
    r = request_get_url(mc_identiy_url+'/me', False)
    if (r.status_code == 401):
        return False
    elif (r.status_code == 200):
        return True
    else:
        r.raise_for_status()
  
def init_arguments():
    global flat
    global mc_identiy_url
    global mc_library_url
    global env
    global auth_token
    
    parser=argparse.ArgumentParser()
    parser.add_argument('--auth', help='myCloud Bearer token. example "Bearer Xus2RupGMYjyRtGBk5rj20RxgQ==')
    parser.add_argument('--env', help='Enviroment: prod, dev2 or test')
    parser.add_argument('-f', action='store_true', help='Adding this option will download all images without creating sub-folders (year/month)')
    args=parser.parse_args()
    
    if (args.f):
        flat = True
    
    if args.env is not None:
        env = args.env
        
    mc_library_url = 'https://library.'+ env + '.mdl.swisscom.ch'
    mc_identiy_url = 'https://identity.' + env + '.mdl.swisscom.ch'
        
    if args.auth is not None:
        auth_token = args.auth
    authenticate()

def init_location():
    global location
    if location == '':
        location = get_current_user_name()
    else:
        location = location + '/' + get_current_user_name()
        
    os.makedirs(location, exist_ok=True)

def request_get_url(url, stream_on):
    payload={}
    headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Authorization': auth_token
    }
    
    r = requests.request("GET", url, headers=headers, data=payload, stream=stream_on)
    
    try: 
        if r.status_code == 401:
            print('No valid access token needed to access myCloud.')
            return r
        else:
            r.raise_for_status()
    except requests.exceptions.HTTPError as e: 
        print (e)
    
    return r
    
def download_single_object(image_meta, current_dir):
    global dm
    
    full_file_path = current_dir + '/' + image_meta['Name']
    
    #check if file already exists
    if os.path.exists(full_file_path):
        return
    
    base_url = mc_library_url + "/download/"
    url = base_url + image_meta['Identifier']
    
    di = DownloadItem(url, full_file_path, image_meta['Length'],0)
    dm.add_item_to_qeue(di)
    #print ('added item to que: ' + image_meta['Name'])
    
def init_timeline_overview():
    url = mc_library_url + "/v2/timeline/index?type=monthly"
    r = request_get_url(url, False)
    timeline_json = r.json()
    total_assets = timeline_json['TotalAssets']
    print(f'Total Photos and videos in myCloud: {total_assets:n}')
    return timeline_json


def download_photos_per_month(month_group):
    global dm
    base_url = mc_library_url + "/v2/timeline/monthly/"
    
    year = str(month_group['Year'])
    month = str(month_group['Month'])
    
    year_month =  year + '/' + month
    url = base_url + year_month
    
    
    #creating directory for current month
    current_dir = location 
    if flat == False:
        current_dir = current_dir + '/' + year + '/' + month
    
    os.makedirs(current_dir, exist_ok=True)
    
    #get file list

    r = request_get_url(url, False)
    images_of_current_month = r.json()

    for image in images_of_current_month:
        download_single_object(image, current_dir)

    helper.print_status(dm.q.qsize(), dm.remaining_size, dm.downloaded_size,speed=dm.get_download_speed(), time_remaining=dm.time_remaining(), description='Added' )
    
def get_current_user_name():
    url = 'https://identity.' + env + '.mdl.swisscom.ch/me'
    r = request_get_url(url, False)
    
    r_me = r.json()
    username = r_me['UserName']
    return username

print('--Welcome to the Photo/Video downloader for Swisscom myCloud.--')

init_arguments()
init_location()

dm = DownloadManager(5, auth_token)

timeline_json = init_timeline_overview()
time_started = datetime.now()

for group in timeline_json['Groups']:
    download_photos_per_month(group)
    
    
    
