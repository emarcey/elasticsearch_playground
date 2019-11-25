import os
import time
from datetime import datetime

def make_filename(
    dir_name: str, file_description: str, file_extension: str, with_timestamp: bool=True
) -> str:
    return f"{os.getcwd()}/{dir_name}/{file_description}_{datetime.utcfromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')}.{file_extension}"
