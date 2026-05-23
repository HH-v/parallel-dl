import time
import functools

def retry(max_attempts=3, delay=1, backoff=2, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt >= max_attempts:
                        raise
                    time.sleep(delay * (backoff ** (attempt - 1)))
            return None
        return wrapper
    return decorator

class ResumeInfo:
    def __init__(self):
        self.downloaded_chunks = set()
        self.partial_file = None
    
    def save(self, path):
        import json
        with open(path, "w") as f:
            json.dump({"chunks": list(self.downloaded_chunks)}, f)
    
    @classmethod
    def load(cls, path):
        import json
        info = cls()
        with open(path) as f:
            data = json.load(f)
            info.downloaded_chunks = set(data["chunks"])
        return info
