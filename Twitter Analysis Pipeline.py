{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Twitter Analysis Pipeline\n",
    "\n",
    "![](https://www.evernote.com/l/AAFtiWq4lUNNiqyswF72dUV3f_7Geq_TcykB/image.png)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "! pip install boto3 pymongo twitter --quiet"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import lib "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Write Tweets to S3"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Create a Tweet Iterator"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "consumer_key    = None\n",
    "consumer_secret = None\n",
    "token           = None\n",
    "token_secret    = None\n",
    "bounding_box    = \"-118.5137323688,34.0001996344,-118.4702449172,34.0331651696\"\n",
    "\n",
    "tweet_iterator  = lib.create_tweet_iterator(token, \n",
    "                                            token_secret,\n",
    "                                            consumer_key,\n",
    "                                            consumer_secret,\n",
    "                                            bounding_box)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "tweets = [next(tweet_iterator) for _ in range(50)]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "tweets_2 = []\n",
    "for _ in range(50):\n",
    "    tweets_2.append(next(tweet_iterator))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Write list of tweets to JSON file on disk"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import json \n",
    "\n",
    "username = 'joshua'\n",
    "\n",
    "filename = lib.create_timestamped_filename(username)\n",
    "with open(filename, 'w') as outfile:\n",
    "    json.dump(tweets, outfile)\n",
    "    \n",
    "filename = lib.create_timestamped_filename(username)\n",
    "with open(filename, 'w') as outfile:\n",
    "    json.dump(tweets_2, outfile)    "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Write Tweet Files to S3, Step 1 - Create a Boto Client to S3\n",
    "\n",
    "https://boto3.readthedocs.io"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "s3_client = lib.create_boto_client()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from os import listdir"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "current_directory = listdir()\n",
    "current_directory = [file for file in current_directory if 'tweets-joshua' in file]\n",
    "current_directory"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from os import rename"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Write Tweet Files to S3, Step 2 - Write a file to S3"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "S3_BUCKET = 'uclax-data-science'\n",
    "\n",
    "for filename in current_directory:\n",
    "    lib.write_file_to_S3(s3_client, filename, S3_BUCKET)\n",
    "    old_filename = filename\n",
    "    filename = filename.replace('.json', '')\n",
    "    filename = filename + '-processed.json'\n",
    "    rename(old_filename, filename)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "current_directory = listdir()\n",
    "current_directory = [file for file in current_directory if 'tweets-joshua' in file]\n",
    "current_directory"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### List Files on S3"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "s3_files = lib.list_files_in_S3_bucket(s3_client, S3_BUCKET)\n",
    "s3_files = [file for file in s3_files if 'tweets-joshua' in file]\n",
    "s3_files"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Write Tweets to Mongo"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Read an object from S3"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "S3_BUCKET = 'uclax-data-science'\n",
    "key = s3_files[1]\n",
    "\n",
    "tweets_from_s3 = lib.read_object_from_S3(s3_client, key, S3_BUCKET)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Write Tweets to Mongo"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from pymongo.errors import DuplicateKeyError"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "collection_client = lib.create_mongo_client_to_database_collection('twitter', 'tweets')\n",
    "for tweet in tweets_from_s3:\n",
    "    try:\n",
    "        collection_client.insert_one(tweet)\n",
    "    except DuplicateKeyError as e:\n",
    "        print(e)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "collection_client = lib.create_mongo_client_to_database_collection('twitter', 'tweets')\n",
    "for tweet in tweets_from_s3:\n",
    "    try:\n",
    "        collection_client.insert_one(tweet)\n",
    "    except DuplicateKeyError as e:\n",
    "        print(e)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "for key in s3_files[2:]:\n",
    "    for tweet in tweets_from_s3:\n",
    "        try:\n",
    "            collection_client.insert_one(tweet)\n",
    "        except DuplicateKeyError as e:\n",
    "            print(e)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## One More Time"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "tweets = [next(tweet_iterator) for _ in range(50)]\n",
    "\n",
    "filename = lib.create_timestamped_filename(username)\n",
    "with open(filename, 'w') as outfile:\n",
    "    json.dump(tweets, outfile)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "current_directory = listdir()\n",
    "current_directory = [file for file in current_directory \n",
    "                     if ('tweets-joshua' in file) and ('processed' not in file)]\n",
    "current_directory"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "for filename in current_directory:\n",
    "    lib.write_file_to_S3(s3_client, filename, S3_BUCKET)\n",
    "    old_filename = filename\n",
    "    filename = filename.replace('.json', '')\n",
    "    filename = filename + '-processed.json'\n",
    "    rename(old_filename, filename)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "s3_files = lib.list_files_in_S3_bucket(s3_client, S3_BUCKET)\n",
    "s3_files = [file for file in s3_files if 'tweets-joshua' in file]\n",
    "s3_files"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "s3_files[-1]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "key = s3_files[-1]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "tweets_from_s3 = lib.read_object_from_S3(s3_client, key, S3_BUCKET)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "collection_client.insert_many(tweets_from_s3)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Automate It"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from datetime import datetime"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "TOKEN           = \"12270642-8ggOVEjcQ7DAP2VCCZbXYoRtiOf0rngzrsyb82h7k\"\n",
    "TOKEN_SECRET    = \"85KnJJBbdvhZyGhOVLPwk47x2IAHaLEFGhNJdrHXo1Tv8\"\n",
    "CONSUMER_KEY    = \"Jt9H3ve228Tl8yafi4Ip8Iwbw\"\n",
    "CONSUMER_SECRET = \"xXxkq7QM1D7K1w0tFKRIYYviS2EQ288jzbbiwzEYYRQrMyvCDN\"\n",
    "BOUNDING_BOX    = \"-118.5137323688,34.0001996344,-118.4702449172,34.0331651696\"\n",
    "\n",
    "DATABASE        = 'twitter'\n",
    "COLLECTION      = 'tweets'\n",
    "USERNAME        = 'joshua'\n",
    "\n",
    "S3_BUCKET       = 'uclax-data-science'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "tweet_iterator    = lib.create_tweet_iterator(TOKEN, TOKEN_SECRET, \n",
    "                                              CONSUMER_KEY, CONSUMER_SECRET, BOUNDING_BOX)\n",
    "s3_client         = lib.create_boto_client()\n",
    "collection_client = lib.create_mongo_client_to_database_collection(DATABASE, COLLECTION)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def timestamp():\n",
    "    now = datetime.now().strftime('%D %H:%M:%S')\n",
    "    print(now, end=' | ')\n",
    "    print('Collecting Tweets', end=' | ')\n",
    "    \n",
    "def collect_tweets(n=50):\n",
    "    tweets = [next(tweet_iterator) for _ in range(n)]\n",
    "    print('{} Tweets'.format(n), end=' | ')\n",
    "    return tweets\n",
    "    \n",
    "def write_to_disk(tweets):\n",
    "    filename = lib.create_timestamped_filename(USERNAME) \n",
    "    with open(filename, 'w') as outfile:\n",
    "        json.dump(tweets, outfile)    \n",
    "    print('Written to Disk', end=' | ')\n",
    "    return filename\n",
    "    \n",
    "def write_to_S3(filename):   \n",
    "    lib.write_file_to_S3(s3_client, filename, S3_BUCKET)\n",
    "    old_filename = filename\n",
    "    filename = filename.replace('.json', '')\n",
    "    filename = filename + '-processed.json'\n",
    "    rename(old_filename, filename)\n",
    "    print('Written to S3', end=' | ')\n",
    "    \n",
    "def insert_to_mongo(key):\n",
    "    tweets_from_s3 = lib.read_object_from_S3(s3_client, key, S3_BUCKET)    \n",
    "    collection_client.insert_many(tweets_from_s3)\n",
    "    print('Inserted to Mongo')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "while True:\n",
    "    timestamp()\n",
    "    tweets = collect_tweets()\n",
    "    filename = write_to_disk(tweets)\n",
    "    write_to_S3(filename)\n",
    "    insert_to_mongo(filename)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}