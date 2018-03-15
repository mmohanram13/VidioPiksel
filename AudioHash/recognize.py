import AudioHash.fingerprint as fingerprint
import AudioHash.decoder as decoder
import numpy as np
import pyaudio
import time


class BaseRecognizer(object):

    def __init__(self, AudioHash):
        self.AudioHash = AudioHash
        self.Fs = fingerprint.DEFAULT_FS

    def _recognize(self, *data):
        matches = []
        for d in data:
            matches.extend(self.AudioHash.find_matches(d, Fs=self.Fs))
        return self.AudioHash.align_matches(matches)

    def recognize(self):
        pass  # base class does nothing


class FileRecognizer(BaseRecognizer):
    def __init__(self, AudioHash):
        super(FileRecognizer, self).__init__(AudioHash)

    def recognize_file(self, filename):
        frames, self.Fs, file_hash = decoder.read(filename, self.AudioHash.limit)

        t = time.time()
        match = self._recognize(*frames)
        t = time.time() - t

        if match:
            match['match_time'] = t

        return match

    def recognize(self, filename):
        return self.recognize_file(filename)
