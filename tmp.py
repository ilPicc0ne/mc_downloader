def human_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    
    time = F'{h:d}:{m:02d}:{s:02d}'
    print(time)
    return time

human_time(180)