"""Command-line interface for parallel-dl."""

import argparse
import logging
from .downloader import Downloader


def main():
    parser = argparse.ArgumentParser(
        description="Multi-threaded parallel file downloader"
    )
    parser.add_argument("url", help="URL to download")
    parser.add_argument("-o", "--output", help="Output filename")
    parser.add_argument("-t", "--threads", type=int, default=4,
                        help="Number of download threads (default: 4)")
    parser.add_argument("-c", "--chunk-size", type=int, default=1048576,
                        help="Chunk size in bytes (default: 1MB)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable verbose logging")
    
    args = parser.parse_args()
    
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    
    dl = Downloader(
        url=args.url,
        dest=args.output,
        threads=args.threads,
        chunk_size=args.chunk_size,
    )
    
    try:
        dl.download()
    except KeyboardInterrupt:
        dl.cancel()
        raise SystemExit(1)
    except Exception as e:
        logging.error(f"Download failed: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
