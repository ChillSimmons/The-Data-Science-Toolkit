import boto3
import json
from datetime import datetime
from pandas import DataFrame
from pymongo import MongoClient
from twitter import TwitterStream
from twitter import OAuth

def create_boto_client():
    s3 = boto3.resource('s3')

    AWS_ACCESS_KEY_ID = 'AKIAJYKWZL555ZQNFSIA'
    AWS_SECRET_ACCESS_KEY = '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'

    client = boto3.client('s3',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    return client

def create_mongo_client_to_database_collection(database, collection):
    client = MongoClient('18.236.138.158', 27016)
    database = client.get_database(database)
    collection = database.get_collection(collection)
    return collection

def create_tweet_iterator(token, token_secret, consumer_key, consumer_secret, bounding_box):
    oauth = OAuth(token, token_secret, consumer_key, consumer_secret)
    twitter_stream = TwitterStream(auth=oauth)
    tweet_iterator = twitter_stream.statuses.filter(locations=bounding_box)
    return tweet_iterator

def create_timestamped_filename(username):
    timestamp_str = str(datetime.now())
    timestamp_str = (timestamp_str.replace(' ', '_')
                                  .replace('.', '-')
                                  .replace(':', '-'))
    filename = "tweets-" + username + '-' + timestamp_str + ".json"
    return filename

def read_object_from_S3(client, key, bucket):

    object_reference = client.get_object(Key=key,
                                         Bucket=bucket)
    object_body = object_reference['Body']
    tweet_data = json.loads(object_body.read().decode())
    return tweet_data

def write_file_to_S3(client, filename, s3_bucket):
    with open(filename) as infile:
        json_data=infile.read()
        client.put_object(Key=filename,
                          Body=json_data,
                          Bucket=s3_bucket)

def list_files_in_S3_bucket(client, s3_bucket):
    objects = client.list_objects(Bucket=s3_bucket)
    objects_df = DataFrame(objects['Contents'])
    return list(objects_df.Key.values)
