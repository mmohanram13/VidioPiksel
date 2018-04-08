from AudioHash.database import get_database, Database
import AudioHash.decoder as decoder
from AudioHash import fingerprint
import os
import traceback
import sys


class AudioHash(object):

    SONG_ID = "song_id"
    SONG_NAME = 'song_name'
    CONFIDENCE = 'confidence'
    MATCH_TIME = 'match_time'
    OFFSET = 'offset'
    OFFSET_SECS = 'offset_seconds'

    def __init__(self, config):
        super(AudioHash, self).__init__()

        self.config = config

        # initialize db
        db_cls = get_database()

        self.db = db_cls(**config.get("database", {}))
        self.db.setup()

        # if we should limit seconds fingerprinted,
        # None|-1 means use entire track
        self.limit = self.config.get("fingerprint_limit", None)
        if self.limit == -1:  # for JSON compatibility
            self.limit = None
        self.get_fingerprinted_songs()

    def get_fingerprinted_songs(self):
        # get songs previously indexed
        self.songs = self.db.get_songs()
        self.songhashes_set = set()  # to know which ones we've computed before
        for song in self.songs:
            song_hash = song[Database.FIELD_FILE_SHA1]
            self.songhashes_set.add(song_hash)

    def fingerprint_file(self, filepath, song_name=None):
        songname = decoder.path_to_songname(filepath)
        song_hash = decoder.unique_hash(filepath)
        song_name = song_name or songname
        # don't refingerprint already fingerprinted files
        #if song_hash in self.songhashes_set:
        #    print("%s already fingerprinted, continuing..." % song_name)
        #else:
        song_name, hashes, file_hash = _fingerprint_worker(
            filepath,
            self.limit,
            song_name=song_name
        )
        sid = self.db.insert_song(song_name, file_hash)
        print( "Completed inserting songs" )
        self.db.insert_hashes(sid, hashes)
        print( "Completed inserting hashes" )
        self.db.set_song_fingerprinted(sid)
        print( "Completed setting song as fingerprinted" )
        self.get_fingerprinted_songs()
        print( "Completed getting fingerprinted songs" )
        return None

    def find_matches(self, samples, Fs=fingerprint.DEFAULT_FS):
        hashes = fingerprint.fingerprint(samples, Fs=Fs)
        return self.db.return_matches(hashes)

    def align_matches(self, matches):
        """
            Finds hash matches that align in time with other matches and finds
            consensus about which hashes are "true" signal from the audio.

            Returns a dictionary with match information.
        """
        # align by diffs
        diff_counter = {}
        largest = 0
        i = 0
        largest_count = 0
        song_id = -1
        song_list = []
        song = {}
        for tup in matches:
            sid, diff = tup
            if diff not in diff_counter:
                diff_counter[diff] = {}
            if sid not in diff_counter[diff]:
                diff_counter[diff][sid] = 0
            diff_counter[diff][sid] += 1

            if diff_counter[diff][sid] > 2500:#largest_count:
                largest = diff
                largest_count = diff_counter[diff][sid]
                if sid not in song_list:
                    song_list.append(sid)
                song_id = sid

        for song_id in song_list:
            i = i + 1;
            song1 = self.db.get_song_by_id(song_id)
            if song1:
                songname = song1.get(AudioHash.SONG_NAME, None)
            else:
                return None
            song [i] = {'song_id': song_id, 'song_name': songname}

        '''# extract idenfication
        song = self.db.get_song_by_id(song_id)
        if song:
            # TODO: Clarify what `get_song_by_id` should return.
            songname = song.get(AudioHash.SONG_NAME, None)
            print(songname)
        else:
            return None

        # return match info
        nseconds = round(float(largest) / fingerprint.DEFAULT_FS *
                         fingerprint.DEFAULT_WINDOW_SIZE *
                         fingerprint.DEFAULT_OVERLAP_RATIO, 5)
        song = {
            AudioHash.SONG_ID : song_id,
            AudioHash.SONG_NAME : songname,
            #AudioHash.CONFIDENCE : largest_count,
            #AudioHash.OFFSET : int(largest),
            #AudioHash.OFFSET_SECS : nseconds,
            #Database.FIELD_FILE_SHA1 : song.get(Database.FIELD_FILE_SHA1, None),
            }'''
        return song

    def recognize(self, recognizer, *options, **kwoptions):
        r = recognizer(self)
        return r.recognize(*options, **kwoptions)


def _fingerprint_worker(filename, limit=None, song_name=None):
    # Pool.imap sends arguments as tuples so we have to unpack
    # them ourself.
    try:
        filename, limit = filename
    except ValueError:
        pass

    songname, extension = os.path.splitext(os.path.basename(filename))
    song_name = song_name or songname
    channels, Fs, file_hash = decoder.read(filename, limit)
    result = set()
    channel_amount = len(channels)

    for channeln, channel in enumerate(channels):
        # TODO: Remove prints or change them into optional logging.
        print("Fingerprinting channel %d/%d for %s" % (channeln + 1,
                                                       channel_amount,
                                                       filename))
        hashes = fingerprint.fingerprint(channel, Fs=Fs)
        print("Finished channel %d/%d for %s" % (channeln + 1, channel_amount,
                                                 filename))
        result |= set(hashes)

    return song_name, result, file_hash
