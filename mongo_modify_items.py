import pymongo
from bson.json_util import dumps

import mongo_config


class MongoRepository:
    def __init__(self, target_mongo_db, target_mongo_table):
        self.mongo_client = pymongo.MongoClient(
            "mongodb+srv://{username}:{password}@mongodb-itzartechnicalt.mddck.mongodb.net/{endpoint}?retryWrites=true&w=majority".format(
                username=mongo_config.db_username,
                password=mongo_config.db_password,
                endpoint=mongo_config.db_endpoint
            )
        )
        self.db = self.mongo_client[target_mongo_db]
        self.event_collection = self.db[target_mongo_table]

    def insert_mongo_event_counter_json(self, event_data):
        if event_data.get('EventId', '') != '':
            entity_id = {'EventId': event_data.get('EventId', ''),
                         'EventDay': event_data.get('EventDay', '')}
            return self.event_collection.update_one(entity_id,
                                                    {"$set": {'EventCount': event_data.get('EventCount', 1)}},
                                                    upsert=True).raw_result
        else:
            print("No EventId, skipping record")

    def query_mongo_by_entityid(self, entity_id):
        results = self.event_collection.find({'EventId': entity_id})
        print("Query: %s found: %d document(s)" % (entity_id, results.count()))
        return dumps(results.sort("EventDay", pymongo.ASCENDING))

    def query_mongo_by_entityid_date(self, entity_id, entity_date):
        entity_id = {'EventId': entity_id, 'EventDay': {"$gt": int(entity_date)}}
        results = self.event_collection.find(entity_id)
        print("Query: %s found: %d document(s)" % (entity_id, results.count()))
        return dumps(results.sort("EventDay", pymongo.ASCENDING))

    def upsert_mongo_event_counter_json(self, event_data):
        entity_id = {'EventId': event_data.get('EventId', ''),
                     'EventDay': int(event_data.get('EventDay', 0))}
        if event_data.get('EventId', '') != '':
            self.event_collection.update_one(entity_id,
                                             {"$inc": {"EventCount":
                                                           event_data.get('EventCount', 1)}},
                                             upsert=True).raw_result
        else:
            print("No EventId, skipping record")

    def delete_mongo_event_counter_json(self, entity_id):
        return dumps(self.event_collection
                     .delete_many({'EventId': entity_id})
                     .deleted_count)


def main():
    mongo_db = 'sample_mflix'  # DB to PUT
    table_name = 'sessions'  # Table to PUT
    mongo_repo = MongoRepository(mongo_db, table_name)
    event_sample = {'EventId': '324', 'EventDay': 20171010}  # Rows-values to PUT in the Table
    print(mongo_repo.upsert_mongo_event_counter_json(event_sample))


if __name__ == '__main__':
    main()
