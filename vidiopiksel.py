#!/usr/bin/env python3

import sys
import os
import pipes
import json
import argparse
import warnings

from AudioHash import AudioHash
from AudioHash.recognize import FileRecognizer

warnings.filterwarnings("ignore")
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

    # create a AudioHash instance
    return AudioHash(config)

def video_to_audio(filePath):
    try:
        directory,fileName = os.path.split(filePath)
        file, file_extension = os.path.splitext(fileName)
        pipes.quote(directory+file)
        new_temp = 'mkdir Temp'
        video_to_mp3 = 'ffmpeg -i ' + filePath + ' ' + 'Temp\\' + file + '.mp3' + ' -hide_banner'
        os.system(new_temp)
        os.system(video_to_mp3)
        print("Successfully Converted ", fileName, " into MP3 Audio!\n")
        return True
    except OSError:
        print(OSError.reason)
        exit(1)

def video_to_frames(filePath):
    try:
        directory,fileName = os.path.split(filePath)
        file, file_extension = os.path.splitext(fileName)
        pipes.quote(directory+file)
        new_folder = 'mkdir Temp\\' + file
        video_to_jpg = 'ffmpeg -i ' + filePath + ' -vf fps=1 ' + 'Temp\\' + file + '\\' + file + '%06d' + '.jpg' + ' -hide_banner'
        os.system(new_folder)
        os.system(video_to_jpg)
        print("Successfully Converted ", fileName, " into Individual Frame per second!")
        return True
    except OSError:
        print(OSError.reason)
        exit(1)

def main():

    if len(sys.argv) < 3:
        print('Wrong command usage')
        exit(1)

    else:
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--fingerprint')
        parser.add_argument('-r', '--recognize')
        args = parser.parse_args()

        if not args.fingerprint and not args.recognize:
            print('Wrong command usage')
            sys.exit(0)

        filePath,file=os.path.split(sys.argv[2])
        print(filePath + "    " + file)

        try:
            if os.path.exists(sys.argv[2]):
                print("File Found!")
        except OSError:
            print(OSError.reason)
            exit(1)

        file, file_extension = os.path.splitext(file)

        if video_to_audio(sys.argv[2]):
            aud = init(config_file)
            filemp3 = 'Temp\\' + file +'.mp3'
            if args.fingerprint:
                if os.path.isdir(filemp3):
                    print("Can fingerprint only a single file!")
                    sys.exit(2)
                aud.fingerprint_file(filemp3)
                print('\nCompleted Audio Fingerprinting')
                os.system('del ' + filemp3)

            elif args.recognize:
                # Recognize audio source
                os.system('cls')
                print("\nStarted Identifying...\n")
                output = None
                output = aud.recognize(FileRecognizer, filemp3)
                print(output)
                os.system('del ' + filemp3)
                os.system('rmdir Temp')
                sys.exit(3)

        if video_to_frames(sys.argv[2]):
            file_images = 'Temp\\' + file
            #Image Fingerprinting Code Goes Here
            os.system('del ' + file_images)
            os.system('rmdir ' + file_images)
            os.system('rmdir Temp')
            sys.exit(4)

if __name__ == '__main__':
    main()
