import os
import queue
import threading
from datetime import datetime



import requests

import helper




class DownloadItem:
    def __init__(self, url, full_file_path, size, retries, current_dir, creation_date):
        self.url = url
        self.full_file_path = full_file_path
        self.size = size
        self.retries = retries
        self.current_dir = current_dir
        self.creation_date = int(creation_date)


class DownloadManager:

    def __init__(self, num_threads, auth_token):
        self.q = queue.Queue(maxsize=0)
        self.auth_token = auth_token
        self.remaining_size = 0
        self.downloaded_size = 0
        self.time_started = datetime.now()

        for t in range(num_threads):
            threading.Thread(target=self.worker, args=str(t)).start()

    # in bytes per second
    def get_download_speed(self):
        seconds = (datetime.now() - self.time_started).total_seconds()
        speed = self.downloaded_size / seconds
        return speed

    def time_remaining(self):
        if (self.get_download_speed() > 0):
            return int(self.remaining_size / self.get_download_speed())
        else:
            return 0

    def worker(self, name):
        payload = {}
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Authorization': self.auth_token,
            'User-Agent': 'Photo Downloader POC - python'
        }

        while True:
            item = self.q.get()
            r = requests.request("GET", item.url, headers=headers, data=payload)
            if r.status_code == 200:
                os.makedirs(item.current_dir, exist_ok=True)
                with open(item.full_file_path, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)
                        
                helper.set_creation_Date(item.full_file_path, item.creation_date)
                self.downloaded_size += item.size
                self.remaining_size -= item.size
                
                
                helper.print_status(self.q.qsize(), self.remaining_size, self.downloaded_size,
                                    speed=self.get_download_speed(), time_remaining=self.time_remaining(),
                                    description='Downloaded')
            elif r.status_code == 401:
                print('Authentication failed')
            else:
                r.raise_for_status()
            self.q.task_done()

    def add_item_to_qeue(self, download_item):
        self.q.put(download_item)
        self.remaining_size = self.remaining_size + download_item.size
