from py_spark_test import PySparkTest
from operator import add
import unittest
import os
from pyspark.sql.types import StructType, StructField, StringType, FloatType
from pyspark.sql import SQLContext
from twitter_stream import TwitterStreamConnector
from pyspark.sql import SQLContext

class TestTwitter(PySparkTest):
    def test_basic(self):
        mock_list = [{"id": "1234",
                        "text": "Great concert.", 
                        "created_at": 1234.0, 
                        "username": "tarkovsky", 
                        "user_screenname": "zerkalo",
                        "user_id": "98765",
                        "user_created_at": 14.0}, 
                     {"id": "5678",
                        "text": "Bad concert.", 
                        "created_at": 67.0, 
                        "username": "kubrick", 
                        "user_screenname": "barry lyndon",
                        "user_id": "34567",
                        "user_created_at": 987.0}]

        stream_connector = TwitterStreamConnector(os.environ.get('TWITTER_API_KEY'), os.environ.get('TWITTER_API_SECRET'), os.environ.get('TWITTER_ACCESS_TOKEN'), os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'))

        sorted_mock_schema = StructType([
            StructField('id', StringType(), True),
            StructField('text', StringType(), True),
            StructField('created_at', FloatType(), True),
            StructField('username', StringType(), True),
            StructField('user_screenname', StringType(), True),
            StructField('user_id', StringType(), True),
            StructField('user_created_at', FloatType(), True)
            ])

        expected = [("5678", "Bad concert.",  67.0,  "kubrick",  "barry lyndon", "34567", 987.0),
        ("1234", "Great concert.", 1234.0, "tarkovsky", "zerkalo", "98765", 14.0), ]
        
        sqlContextTest = SQLContext(self.spark.sparkContext)
        df = sqlContextTest.createDataFrame(expected, sorted_mock_schema)

        test_df = stream_connector.sort_file(mock_list, sqlContextTest, sorted_mock_schema)

        print(test_df.show())

        print(df.show())
        self.assertEqual(test_df.collect(), df.collect())

if __name__ == '__main__':
    unittest.main()