from __future__ import absolute_import


class Database(object):
    FIELD_FILE_SHA1 = 'file_sha1'
    FIELD_SONG_ID = 'song_id'
    FIELD_SONGNAME = 'song_name'
    FIELD_OFFSET = 'offset'
    FIELD_HASH = 'hash'

    def __init__(self):
        super(Database, self).__init__()

    def before_fork(self):
        """
        Called before the database instance is given to the new process
        """
        pass

    def after_fork(self):
        """
        Called after the database instance has been given to the new process

        This will be called in the new process.
        """
        pass

    def setup(self):
        """
        Called on creation or shortly afterwards.
        """
        pass

    def empty(self):
        """
        Called when the database should be cleared of all data.
        """
        pass

    def delete_unfingerprinted_songs(self):
        """
        Called to remove any song entries that do not have any fingerprints
        associated with them.
        """
        pass

    def get_num_songs(self):
        """
        Returns the amount of songs in the database.
        """
        pass

    def get_num_fingerprints(self):
        """
        Returns the number of fingerprints in the database.
        """
        pass

    def set_song_fingerprinted(self, sid):
        """
        Sets a specific song as having all fingerprints in the database.

        sid: Song identifier
        """
        pass

    def get_songs(self):
        """
        Returns all fully fingerprinted songs in the database.
        """
        pass

    def get_song_by_id(self, sid):
        """
        Return a song by its identifier

        sid: Song identifier
        """
        pass

    def insert(self, hash, sid, offset):
        """
        Inserts a single fingerprint into the database.

          hash: Part of a sha1 hash, in hexadecimal format
           sid: Song identifier this fingerprint is off
        offset: The offset this hash is from
        """
        pass

    def insert_song(self, song_name):
        """
        Inserts a song name into the database, returns the new
        identifier of the song.

        song_name: The name of the song.
        """
        pass

    def query(self, hash):
        """
        Returns all matching fingerprint entries associated with
        the given hash as parameter.

        hash: Part of a sha1 hash, in hexadecimal format
        """
        pass

    def get_iterable_kv_pairs(self):
        """
        Returns all fingerprints in the database.
        """
        pass

    def insert_hashes(self, sid, hashes):
        """
        Insert a multitude of fingerprints.

           sid: Song identifier the fingerprints belong to
        hashes: A sequence of tuples in the format (hash, offset)
        -   hash: Part of a sha1 hash, in hexadecimal format
        - offset: Offset this hash was created from/at.
        """
        pass

    def return_matches(self, hashes):
        """
        Searches the database for pairs of (hash, offset) values.

        hashes: A sequence of tuples in the format (hash, offset)
        -   hash: Part of a sha1 hash, in hexadecimal format
        - offset: Offset this hash was created from/at.

        Returns a sequence of (sid, offset_difference) tuples.

                      sid: Song identifier
        offset_difference: (offset - database_offset)
        """
        pass

def get_database():
    database_type = "mysql"

    for db_cls in Database.__subclasses__():
        if db_cls.type == database_type:
            return db_cls

    raise TypeError("Unsupported database type supplied.")

import AudioHash.database_sql
