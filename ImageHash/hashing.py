from ImageHash.database import get_database,Database
import ImageHash.decoder as decoder
import os
import traceback
import sys

class ImageHash(object):

    IMAGE_ID = "img_id"
    IMAGE_NAME = "img_name"
    CONFIDENCE = "confidence"

    def __init__(self,config):
        super(ImageHash, self).__init__()

        self.config = config
        #initialize db
        db_cls = get_database()

        self.db = db_cls(**config.get("database",{}))
        self.db.setup()
        
