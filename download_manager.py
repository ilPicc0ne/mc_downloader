
import threading, queue
import time
import random
import requests
import helper

class DownloadItem:
    def __init__(self, url, full_file_path, size, retries):
        self.url = url
        self.full_file_path = full_file_path
        self.size = size
        self.retries = retries
        
class DownloadManager:
    
    
    
    def __init__(self, num_threads, auth_token):
        self.q = queue.Queue(maxsize=0)
        self.auth_token = auth_token
        self.q_total_size = 0
        self.downloaded_size = 0
        
        for t in range(num_threads):
            print(f'dispatchin worker {t}')
            threading.Thread(target=self.worker, args=str(t)).start()

    def get_download_speed():
        seconds = (datetime.now()-time_started).total_seconds()
        speed = str(round((size_downloaded/seconds)/1024/1024,2)) + ' MB/s'
        return speed

    def worker(self, name):
        payload={}
        headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Authorization': self.auth_token
        }
        print(f'worker {name} ready')
        while True:
            item = self.q.get()
            r = requests.request("GET", item.url, headers=headers, data=payload)
            if r.status_code == 200:
                with open(item.full_file_path, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)
                self.downloaded_size += item.size
                self.q_total_size -= item.size
                helper.print_status(self.q.qsize(), self.q_total_size, self.downloaded_size, 'Image/Video Downloaded')
            elif r.status_code == 401:
                print('Authentication failed')
            
            self.q.task_done()

    def add_item_to_qeue(self, download_item):
        self.q.put(download_item)
        self.q_total_size = self.q_total_size+ download_item.size



