#!/usr/bin/env python3

import sys
import os
import pipes
import json
import argparse

'''from AudioFingerprinter import AudioFingerprinter
from AudioFingerprinter.recognize import FileRecognizer

config_file = "dbconfig.cnf"


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
    return AudioFingerprinter(config)'''

def video_to_audio(filePath):
    try:
        directory,fileName = os.path.split(filePath)
        file, file_extension = os.path.splitext(fileName)
        pipes.quote(directory+file)
        video_to_wav = 'ffmpeg -i ' + filePath + ' ' + 'Temp\\' + file + '.wav' + ' -hide_banner'
        os.system(video_to_wav)
        print("Successfully Converted ", fileName, " into MP3 Audio!")
        return True
    except OSError:
        print(OSError.reason)
        exit(1)

def video_to_frames(filePath):
    try:
        directory,fileName = os.path.split(filePath)
        file, file_extension = os.path.splitext(fileName)
        pipes.quote(directory+file)
        new_folder = 'mkdir temp\\' + file
        video_to_jpg = 'ffmpeg -i ' + filePath + ' -vf fps=1 ' + 'Temp\\' + file + '\\' + file + '%06d' + '.jpg' + ' -hide_banner'
        os.system(new_folder)
        os.system(video_to_jpg)
        print("Successfully Converted ", fileName, " into Individual Frame per second!")
        return True
    except OSError:
        print(OSError.reason)
        exit(1)

def main():

    if len(sys.argv) < 2:
        print('Wrong command usage')
        exit(1)

    else:
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--fingerprint')
        parser.add_argument('-r', '--recognize')

        '''if not args.fingerprint and not args.recognize:
            print('Wrong command usage')
            sys.exit(0)'''

        file,filePath=os.path.split(sys.argv[1])
        print(file + "    " + filePath)
        
        try:
            if os.path.exists(sys.argv[1]):
                print("File Found!")
        except OSError:
            print(OSError.reason)
            exit(1)

        if video_to_audio(sys.argv[1]):
            '''aud = init(config_file)
            if args.fingerprint:
                if os.path.isdir(filePath):
                    print("Can fingerprint only a single file!")
                    sys.exit(1)
                aud.fingerprint_file(filePath)

            elif args.recognize:
            # Recognize audio source
                output = None
                output = aud.recognize(FileRecognizer, filePath)
                if len(output)==1:
                    print(output)
                    sys.exit(0)'''

        if video_to_frames(sys.argv[1]):
            sys.exit(0)
         
if __name__ == '__main__':
    main()