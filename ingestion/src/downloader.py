import hashlib
import os
import requests
from tqdm import tqdm

from config import SOURCE_URL

def download_file(url, destination):
    temp_path = str(destination) + ".part" #.part means still downloading
    try:
        print(f"Downloading: {url}")
        with requests.get(
            url,
            stream=True, # don't store the whole file in RAM
            timeout=(15, 120) # timeout connection - 15 seconds, one part of data - wait 120 seconds
        ) as response:
            response.raise_for_status() # check http error

            total_size = 0 # to count size of downloaded data

            with open(temp_path, "wb") as file, tqdm(
                total=total_size,
                unit="B",
                unit_scale=True, # Convert Bytes -> KB, MB automatically
                unit_divisor=1024,
                desc=os.path.basename(destination)
            ) as bar:
                # download data file in multiple parts
                for chunk in response.iter_content(
                    chunk_size=8*1024*1024 # roughly 8Mb size
                ):
                    if chunk:
                        file.write(chunk)
                        total_size += len(chunk)
                        bar.update(len(chunk))

            # check the download is completed successfully
            if total_size == 0:
                raise ValueError("Downloaded file is empty!")

            # convert temp file as actual data file
            os.replace(temp_path, destination)

            print(f"Downloaded: {total_size} bytes")

        return destination

    except Exception:
        if os.path.exists(temp_path):
            os.remove(temp_path) # delete temp file

        raise

def calculate_sha256(file_path):
    """Calculates and returns the SHA-256 checksum of a file efficiently by reading it in memory-safe 8MB chunks."""

    sha256 = hashlib.sha256() # sha256 object

    with open(file_path, "rb") as file:

        for chunk in iter(
            lambda: file.read(8 * 1024 * 1024),
            b"" 
        ):
            sha256.update(chunk)

        # b"" means -> until all parts of file are completed

    return sha256.hexdigest() # 64 digit