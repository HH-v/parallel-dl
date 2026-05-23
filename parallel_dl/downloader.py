import os
import threading
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from .chunk import ChunkManager

logger = logging.getLogger(__name__)

class Downloader:
    def __init__(self, url, dest=None, threads=4, chunk_size=1024*1024):
        self.url = url
        self.dest = dest or os.path.basename(url)
        self.threads = threads
        self.chunk_size = chunk_size
    
    def start(self):
        logger.info(f"Starting download: {self.url}")
        return ThreadPoolExecutor(max_workers=self.threads)
    
    def get_file_size(self):
        import requests
        resp = requests.head(self.url, allow_redirects=True)
        size = int(resp.headers.get("content-length", 0))
        if size == 0:
            raise ValueError("Server did not provide content-length")
        return size
    
    def shutdown(self):
        pass
