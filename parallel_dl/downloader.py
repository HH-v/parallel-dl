import os
import requests
import threading
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from .chunk import ChunkManager
from .retry import retry, ResumeInfo
from .progress import ProgressTracker

logger = logging.getLogger(__name__)

class Downloader:
    def __init__(self, url, dest=None, threads=4, chunk_size=1024*1024):
        self.url = url
        self.dest = dest or os.path.basename(url)
        self.threads = threads
        self.chunk_size = chunk_size
        self._progress = None
        self._lock = threading.Lock()
    
    def get_file_size(self):
        resp = requests.head(self.url, allow_redirects=True, timeout=30)
        resp.raise_for_status()
        size = int(resp.headers.get("content-length", 0))
        if size == 0:
            raise ValueError("Server did not provide content-length")
        return size
    
    def download_chunk(self, start, end, dest_fd):
        headers = {"Range": f"bytes={start}-{end}"}
        resp = requests.get(self.url, headers=headers, stream=True, timeout=60)
        resp.raise_for_status()
        data = resp.content
        with self._lock:
            dest_fd.seek(start)
            dest_fd.write(data)
        return len(data)
    
    def download(self):
        size = self.get_file_size()
        logger.info(f"Downloading {self.dest}: {size:,} bytes x {self.threads} threads")
        
        self._progress = ProgressTracker(size, os.path.basename(self.dest))
        chunks = ChunkManager(size, self.chunk_size).split()
        
        with open(self.dest, "wb") as f:
            f.truncate(size)
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                futures = []
                for start, end in chunks:
                    futures.append(executor.submit(self.download_chunk, start, end, f))
                
                for future in as_completed(futures):
                    try:
                        written = future.result()
                        self._progress.update(written)
                    except Exception as e:
                        logger.error(f"Chunk failed: {e}")
                        raise
        
        elapsed = self._progress.close()
        speed = size / elapsed / 1024 / 1024
        logger.info(f"Done in {elapsed:.1f}s ({speed:.1f} MB/s)")
    
    def cancel(self):
        logger.info("Download cancelled")
