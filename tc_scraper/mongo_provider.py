# -*- coding: utf-8 -*-
import pymongo

class MongoProvider(object):

    collection_name = 'tc_posts'

    def __init__(self, uri, database):
        self.mongo_uri = uri
        self.mongo_db = database or 'tc_scraper'

    def get_collection(self):
        self.client = pymongo.MongoClient(self.mongo_uri)
        return self.client[self.mongo_db][self.collection_name]

    def close_connection(self):
        self.client.close()
