import pytest
from parallel_dl.downloader import Downloader

def test_downloader_init():
    dl = Downloader("https://example.com/file.zip")
    assert dl.url == "https://example.com/file.zip"
    assert dl.threads == 4
    assert dl.chunk_size == 1024 * 1024

def test_downloader_custom_dest():
    dl = Downloader("https://example.com/data.bin", dest="./output.bin")
    assert dl.dest == "./output.bin"

def test_downloader_custom_threads():
    dl = Downloader("https://example.com/file.zip", threads=8)
    assert dl.threads == 8
