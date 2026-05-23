class ChunkManager:
    def __init__(self, total_size, chunk_size):
        self.total_size = total_size
        self.chunk_size = chunk_size
        self.downloaded = 0
        self.chunks = []
    
    def split(self):
        chunks = []
        for start in range(0, self.total_size, self.chunk_size):
            end = min(start + self.chunk_size - 1, self.total_size - 1)
            chunks.append((start, end))
        self.chunks = chunks
        return chunks
    
    def mark_complete(self, chunk_idx):
        self.downloaded += 1
