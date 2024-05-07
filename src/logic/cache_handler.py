# Save images etc into a temp dir in the installation folder to keep bandwidth usage low.
# Data should be saved with DATES and maybe some sort of DB to know what is what, from when etc and delete if old.class

# To generate "IDs" for the images make a MD5 hash of the URL and name it like that. so we can check if the
# image is already downloaded.

import os
import datetime
import hashlib


class Cache_handler:
    def __init__(self):
        self.path = ""  # get from config, default is "temp/"
        self.max_age = 604800  # 1 week


cache_handler = Cache_handler()
