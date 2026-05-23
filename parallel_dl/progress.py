import time
from tqdm import tqdm

class ProgressTracker:
    def __init__(self, total, description="Downloading"):
        self.bar = tqdm(
            total=total,
            unit="B",
            unit_scale=True,
            desc=description,
            dynamic_ncols=True,
        )
        self.start_time = time.time()
    
    def update(self, n):
        self.bar.update(n)
    
    def close(self):
        self.bar.close()
        elapsed = time.time() - self.start_time
        return elapsed
