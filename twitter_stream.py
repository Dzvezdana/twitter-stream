#!/usr/bin/env python

import oauth2 as oauth
from  urllib.request import HTTPHandler, HTTPSHandler, OpenerDirector, HTTPError
import urllib.parse
import time
import re
import os
import requests
import json
import pyspark
from pyspark.sql.types import StructType, StructField, StringType, FloatType
from pyspark.sql import SQLContext
import copy, sys
from tweet import Tweet

class TwitterStreamConnector:
    """
    Provides a simple way to connect to the Twitter Streaming Api using the credentials
    provided in the ~/.bash_profile. 
    To get the credentials visit dev.twitter.com. 

    Methods:
    ----------
    twitter_req
    process_stream
    sort_file
    write_file

    Returns:
    ----------
        A TwitteStreamConnector Object
    """

    def __init__(self, consumer_key, consumer_secret, token_key, token_secret):
        """
        Parameters
        ----------
        consumer_key: str 
            Twitter Consumer Key
        consumer_secret: str
            Twitter Consumer Secret
        token_key: str 
            Twitter Access Token
        token_secret: str 
            Twitter Access Token Secret
        """
        self.c_key = consumer_key
        self.c_secret = consumer_secret
        self.t_key = token_key
        self.t_secret = token_secret

    def twitter_req(self, url, method, parameters):
        """
        Constructs, signs, and opens a Twitter request using the provided credentials.
        Parameters
        ----------
        url : str
            Twitter Streaming API Resource URL
        method: str
            HTTP method (GET or POST)
        parameters: list (default is empty)
            parameters that allow a better control of the search results (see https://developer.twitter.com/en/docs/tweets/filter-realtime/api-reference/post-statuses-filter.html)

        Returns
        -------
        response: http.client.HTTPResponse object
            response from the Twitter Streaming API
        """
        _debug = 0
        oauth_token = oauth.Token(key=self.t_key, secret=self.t_secret)
        oauth_consumer = oauth.Consumer(key=self.c_key, secret=self.c_secret)

        signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

        http_method = "GET"
        http_handler  = HTTPHandler(debuglevel=_debug)
        https_handler = HTTPSHandler(debuglevel=_debug)

        req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                                    token=oauth_token,
                                                    http_method=http_method,
                                                    http_url=url, 
                                                    parameters=parameters)

        req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

        headers = req.to_header()

        if http_method == "POST":
            encoded_post_data = req.to_postdata()
        else:
            encoded_post_data = None
            url = req.to_url()

        opener = OpenerDirector()
        opener.add_handler(http_handler)
        opener.add_handler(https_handler)

        try:
            response = opener.open(url, encoded_post_data)
        except HTTPError as e:
            print(e.code)
            print(e.read()) 

        return response

    def process_stream(self):
        """
        Filters the stream based on a keyword. 
        Retrieves the incoming messages for 30 seconds or up to 100 messages, whichever comes first.
        """
        # Max number of tweets
        MAX_TWEET_SIZE = 100
        # Max interval of time
        MAX_TIME_INTERVAL_SECONDS = 30
        # Endpoint
        stream_url = 'https://stream.twitter.com/1.1/statuses/filter.json'
        # Nested list of paramters
        parameters = [['track', 'bieber']]

        # Twitter Stream API response
        response = self.twitter_req(stream_url, "GET", parameters)

        self.schema = StructType([
            StructField('id', StringType(), True),
            StructField('text', StringType(), True),
            StructField('created_at', FloatType(), True),
            StructField('username', StringType(), True),
            StructField('user_screenname', StringType(), True),
            StructField('user_id', StringType(), True),
            StructField('user_created_at', FloatType(), True)
            ])

        tweets_list = []
        
        start_time_seconds = time.time()
        count_tweet_size = 0
        for line in response:
            if line:
                data = json.loads(line)
                tweet = Tweet(data)
                elapsed_time_seconds = time.time() - start_time_seconds
                if elapsed_time_seconds < MAX_TIME_INTERVAL_SECONDS and count_tweet_size < MAX_TWEET_SIZE:
                    count_tweet_size += 1
                    print("Elapsed time: %s" % elapsed_time_seconds)
                    print("Number of input tweets: %s" % count_tweet_size)

                    tweets_list.append(
                        {"id": tweet.id,
                        "text": tweet.text, 
                        "created_at": tweet.created_at, 
                        "username": tweet.username, 
                        "user_screenname": tweet.user_screenname,
                        "user_id": tweet.user_id,
                        "user_created_at": tweet.user_created_at})

                else: 
                    self.sc = pyspark.SparkContext("local", "Twitter App")
                    self.sqlContext = SQLContext(self.sc)
                    df = self.sort_file(tweets_list, self.sqlContext, self.schema)
                    self.write_file(df)
                    sys.exit(0)       

    def sort_file(self, item_list, sql_context, schema):
        """
        Groups messages by user (users sorted chronologically, ascending).
        Sorts messages per user chronologically, ascending.
        Parameters
        ----------
        item_list: list
            extracted tweets
        sql_context
        schema
        """
        df = sql_context.createDataFrame([tuple(tweet_item.values()) for tweet_item in item_list], schema)
        return df.orderBy(["created_at", "user_created_at"]) # Default is ascending

    def write_file(self, ordered_df):
        """
        Writes the results in a tab separated file.
        Parameters
        ----------
        ordered_df
            ordered data frame containing the extracted tweets
        """
        df = ordered_df.withColumn("created_at", ordered_df["created_at"].cast(StringType()))
        df = df.withColumn("user_created_at", df["user_created_at"].cast(StringType()))
        df.coalesce(1).write.format("csv").option("header", "true").mode("append").save("output_file", sep="\t")

if __name__ == '__main__':
    ### Setup access credentials
    CONSUMER_KEY=os.environ.get('TWITTER_API_KEY')
    CONSUMER_SECRET=os.environ.get('TWITTER_API_SECRET')
    TOKEN_KEY=os.environ.get('TWITTER_ACCESS_TOKEN')
    TOKEN_SECRET=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
    
    twitter = TwitterStreamConnector(CONSUMER_KEY, CONSUMER_SECRET, TOKEN_KEY, TOKEN_SECRET)
    twitter.process_stream()