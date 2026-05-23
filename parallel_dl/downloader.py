import os
import requests
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from .chunk import ChunkManager
from .retry import retry, ResumeInfo

logger = logging.getLogger(__name__)

class Downloader:
    def __init__(self, url, dest=None, threads=4, chunk_size=1024*1024):
        self.url = url
        self.dest = dest or os.path.basename(url)
        self.threads = threads
        self.chunk_size = chunk_size
    
    @retry(max_attempts=3, delay=1, exceptions=(requests.RequestException,))
    def get_file_size(self):
        resp = requests.head(self.url, allow_redirects=True, timeout=30)
        resp.raise_for_status()
        size = int(resp.headers.get("content-length", 0))
        if size == 0:
            raise ValueError("Server did not provide content-length")
        return size
    
    @retry(max_attempts=5, delay=0.5, backoff=1.5)
    def download_chunk(self, start, end, dest_fd):
        headers = {"Range": f"bytes={start}-{end}"}
        try:
            resp = requests.get(self.url, headers=headers, stream=True, timeout=60)
        except Exception as e:
            logger.error(f"Chunk {start}-{end} retrying...")
            raise
        resp.raise_for_status()
        dest_fd.seek(start)
        dest_fd.write(resp.content)
        return len(resp.content)
    
    def download(self):
        size = self.get_file_size()
        logger.info(f"File size: {size} bytes, using {self.threads} threads")
        chunks = ChunkManager(size, self.chunk_size).split()
        
        with open(self.dest, "wb") as f:
            f.truncate(size)
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                futures = {
                    executor.submit(self.download_chunk, s, e, f): (s, e) 
                    for s, e in chunks
                }
                for future in as_completed(futures):
                    future.result()
    
    def shutdown(self):
        pass
