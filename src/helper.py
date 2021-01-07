from datetime import datetime
from win32_setctime import setctime
import platform


import os

suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

def humansize(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])

#returns string in MBit per second
def human_speed(bytes_per_second):
    return str(round((bytes_per_second)/1024/1024*8,2)) + ' MBit/s'

def human_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    
    time = F'{h:d}h {m:02d} min'
    return time
    

def print_status(items_in_qeue, size_remaining, size_downloaded, speed, time_remaining, description):
    
    if (speed ==0):
        speed = 'N/A'
    else:
        speed = human_speed(speed)
        
    if (time_remaining == 0):
        time_remaining = 'N/A'
    else:
        time_remaining = human_time(time_remaining)
    
    print(f'Qeue Items: {items_in_qeue:n}, Remaining: {humansize(size_remaining)}, Downloaded: {humansize(size_downloaded)}, Speed: {speed}, Time remaining: {time_remaining},  {description}')
    

def set_creation_Date(file_full_path, new_date_timestamp):
    
    current_os = platform.system()
    new_date = datetime.fromtimestamp(new_date_timestamp)
    
    if current_os in ['Linux', 'Darwin']:
        # set the file creation date with the "-d" switch, which presumably stands for "dodification"
        os.system('SetFile -d "{}" {}'.format(new_date.strftime('%m/%d/%Y %H:%M:%S'), file_full_path))
    elif current_os == 'Windows':
        setctime(file_full_path, new_date_timestamp)
    
    # set the file modification date with the "-m" switch
    #os.system('SetFile -m "{}" {}'.format(new_date.strftime('%m/%d/%Y %H:%M:%S'), file_full_path))
    
    os.utime(file_full_path,(new_date_timestamp, new_date_timestamp))

    