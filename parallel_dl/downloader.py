import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

class Downloader:
    def __init__(self, url, dest=None, threads=4, chunk_size=1024*1024):
        self.url = url
        self.dest = dest or os.path.basename(url)
        self.threads = threads
        self.chunk_size = chunk_size
        self._executor = None
    
    def start(self):
        self._executor = ThreadPoolExecutor(max_workers=self.threads)
        return self._executor
    
    def shutdown(self):
        if self._executor:
            self._executor.shutdown(wait=True)
