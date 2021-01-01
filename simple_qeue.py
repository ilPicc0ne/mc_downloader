
from queue import Queue
from threading import Thread
import time


# Set up some global variables
num_fetch_threads = 5
enclosure_queue = Queue()

# A real app wouldn't use hard-coded data...
feed_urls = [ 'http://www.castsampler.com/cast/feed/rss/guest',
             ]


def downloadEnclosures(i, q):
    while True:
        url = q.get()
        print (f'Thread {i}: Downloading asset nr {url}')
  
        # instead of really downloading the URL,
        # we just pretend and sleep
        time.sleep(i + 2)
        q.task_done()


# Set up some threads to fetch the enclosures
for i in range(num_fetch_threads):
    worker = Thread(target=downloadEnclosures, args=(i, enclosure_queue,))
    worker.setDaemon(True)
    worker.start()
    
for enclosure in range(30):
    print(f'Queuing {enclosure}')
    enclosure_queue.put(enclosure)

        
# Now wait for the queue to be empty, indicating that we have
# processed all of the downloads.
print ('*** Main thread waiting')
enclosure_queue.join()
print ('*** Done')