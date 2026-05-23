from parallel_dl.chunk import ChunkManager

def test_chunk_split_exact():
    cm = ChunkManager(total_size=1000, chunk_size=250)
    chunks = cm.split()
    assert len(chunks) == 4
    assert chunks == [(0, 249), (250, 499), (500, 749), (750, 999)]

def test_chunk_split_uneven():
    cm = ChunkManager(total_size=100, chunk_size=30)
    chunks = cm.split()
    assert len(chunks) == 4
    assert chunks[-1] == (90, 99)
