import argparse
import os
import argparse, sys
from sys import exit
import pathlib
import requests

from datetime import datetime
from download_manager import DownloadManager, DownloadItem
import helper


env = 'prod'
flat = False
jpg = False
username = ''
location = ''
mc_library_url = ''
mc_identity_url = ''
auth_token = ''
auth_ok = False

dm = None


def authenticate():
    global auth_token
    while is_authenticated() == False:
        auth_token = input("Please paste myCloud authentication token (e.g. Bearer Xus2RupGMYjyRtGBk5rj20RxgQ==): ")


def is_authenticated():
    # r = requests.request("GET", mc_identiy_url+'/me', headers=headers, data=payload)
    r = request_get_url(mc_identity_url + '/me', False)
    if r.status_code == 401:
        return False
    elif r.status_code == 200:
        return True
    else:
        r.raise_for_status()


def user_input_config():
    def set_folder_structure():
        global flat
        print('Do you want to create an automatic folder structure (year/month)? (e.g. 2020/12)')
        print('Press \'1\' to download with folder structure (default)')
        print('Press \'2\' to download all in one folder')
        f = input('')
        
        if (f == '1' or f == ''):
            flat = False
            return #default value
        elif f == '2':
            flat = True
        else:
            set_folder_structure()

    def set_download_scope():
        global download_scope
        global location
        print('What do you want to download?')
        print('Press \'1\' for All Photos (default)')
        print('Press \'2\' for all Photos in albums. Will be put in folders with album name.')
        scope = input('')
        if scope == '1' or scope == '':
            download_scope = 'timeline'
            set_folder_structure()
            return  # default value
        elif scope == '2':
            download_scope = 'albums'
            location += '/albums'
        else:
            set_download_scope()

    set_download_scope()


def init_arguments():
    global flat
    global mc_identity_url
    global mc_library_url
    global env
    global auth_token
    global jpg
    
    parser=argparse.ArgumentParser()
    parser.add_argument('--jpg', action='store_true', help='Will download HEIC images as jpg')
    parser.add_argument('--auth', help='myCloud Bearer token. example "Bearer Xus2RupGMYjyRtGBk5rj20RxgQ==')
    parser.add_argument('--env', help='Enviroment: prod, dev2 or test')
    parser.add_argument('-f', action='store_true', help='Adding this option will download all images without creating sub-folders (year/month)')
    
    args=parser.parse_args()
    
    if args.env is not None:
        env = args.env
        
    mc_library_url = 'https://library.'+ env + '.mdl.swisscom.ch'
    mc_identity_url = 'https://identity.' + env + '.mdl.swisscom.ch'
        
    if args.auth is not None:
        auth_token = args.auth
    authenticate()


def init_location():
    global location
    if location == '':
        location = get_current_user_name()
    else:
        location = location + '/' + get_current_user_name()


def request_get_url(url, stream_on):
    payload = {}
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Authorization': auth_token,
        'User-Agent': 'Photo Downloader POC - python'
    }

    r = requests.request("GET", url, headers=headers, data=payload, stream=stream_on)

    try:
        if r.status_code == 401:
            print('No valid access token needed to access myCloud.')
            return r
        else:
            r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)

    return r


def download_single_object(image_meta, current_dir):
    global dm
    
    image_name = image_meta['Name']
    suffix = pathlib.Path(image_name).suffix
    
    if suffix.lower() == '.heic' and jpg:
        base_url = mc_library_url + "/convert/"
        image_name = pathlib.Path(image_name).stem + '.jpg'
    else:
        base_url = mc_library_url + "/download/"
        
    full_file_path = current_dir + '/' + image_name
    
    #os.makedirs(current_dir, exist_ok=True)
    #check if file already exists
    if os.path.exists(full_file_path):
        return
    
    url = base_url + image_meta['Identifier']
    
    creation_date = image_meta['TimestampEpoch']/1000 #from ms to seconds
    
    di = DownloadItem(url, full_file_path, image_meta['Length'],0, current_dir, creation_date)
    dm.add_item_to_qeue(di)
    # print ('added item to que: ' + image_meta['Name'])


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

    year_month = year + '/' + month
    url = base_url + year_month

    # creating directory for current month
    current_dir = location
    if not flat:
        current_dir = current_dir + '/' + year + '/' + month

    # get file list
    r = request_get_url(url, False)
    images_of_current_month = r.json()

    for image in images_of_current_month:
        download_single_object(image, current_dir)

    helper.print_status(dm.q.qsize(), dm.remaining_size, dm.downloaded_size, speed=dm.get_download_speed(),
                        time_remaining=dm.time_remaining(), description='Added')


def download_all_albums():
    def get_all_albums():
        url = mc_library_url + "/v2/photos/projects"
        r = request_get_url(url, stream_on=False)
        return r

    def get_album(album_identifier):
        url = mc_library_url + "/v2/album/" + album_identifier
        r = request_get_url(url, stream_on=False)
        return r.json()

    def download_all_in_album(album_identifier):
        album = get_album(album_identifier)
        current_dir = location + '/' + album['Name']
        for asset in album['Assets']:
            download_single_object(asset, current_dir)

    albums = get_all_albums().json()
    for album in albums:
        if 'Type' not in album:  # excludes special albums (recent etc.)
            if album['Mount'] is None:  # excludes shared albums, can be implemented later
                download_all_in_album(album['Identifier'])


def get_current_user_name():
    url = 'https://identity.' + env + '.mdl.swisscom.ch/me'
    r = request_get_url(url, False)

    r_me = r.json()
    username = r_me['UserName']
    return username


def download_all_timeline():
    timeline_json = init_timeline_overview()
    for group in timeline_json['Groups']:
        download_photos_per_month(group)


print('--Welcome to the Photo/Video downloader for Swisscom myCloud.--')
print()

init_arguments()
init_location()
user_input_config()

dm = DownloadManager(5, auth_token)

if download_scope == 'timeline':
    download_all_timeline()
elif download_scope == 'albums':
    download_all_albums()
