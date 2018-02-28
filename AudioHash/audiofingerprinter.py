#!usr/bin/python3
import os
import sys
import json
import argparse

from AudioFingerprinter import AudioFingerprinter
from AudioFingerprinter.recognize import FileRecognizer

DEFAULT_CONFIG_FILE = "dbconfig.cnf"


def init(configpath):
    """ 
    Load config from a JSON file
    """
    try:
        with open(configpath) as f:
            config = json.load(f)
    except IOError as err:
        print("Cannot open configuration: %s. Exiting" % (str(err)))
        sys.exit(1)

    # create a AudioFingerprinter instance
    return AudioFingerprinter(config)

