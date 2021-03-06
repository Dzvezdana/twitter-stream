# twitter-stream

## Motivation

The application is based on the requirements provided in [INSTRUCTIONS.md](https://github.com/Dzvezdana/twitter-stream/tree/master/INSTRUCTIONS.md).
It supports basic OAuth authentication and subscribes to the [Twitter Streaming API](https://developer.twitter.com/en/docs/tutorials/consuming-streaming-data). Then it:
+ Filters messages that contain the keyword *"bieber"*.

+ Retrieves the incoming messages for 30 seconds or up to 100 messages, whichever comes first.

+ Returns the messages grouped by user (users sorted chronologically, ascending). The messages per user are sorted chronologically, ascending.

+ Writes the output in a tab separated file.

## Requirements
+ Python 3.*
+ requests
+ pyspark 
+ oauth2

You can install the necessary libraries using *pip*.

## How to run
Navigate to the `twitter-stream` directory and run the following command:
```
python twitter_stream.py 
```

**Note**: <br/>
*Twitter API keys* <br/>
To use OAuth authentication go to  http://dev.twitter.com/apps and create an application to get the `consumer_key`, `consumer_secret`, `access_token_key` and `access_token_secret`.
Then set those values in your `~/.bash_profile`.  <br/>
<br/>
The application can be run as Docker container as well:
```
docker build -t twitter_app .
docker run twitter_app
```
**Note**: Add your `consumer_key`, `consumer_secret`, `access_token_key` and `access_token_secret` to the Dockerfile first.

## Output
The application writes the output in a file that is located at `./output_file/*`.  <br/>
Sample output:

    id	text	created_at	username	user_screenname	user_id	user_created_at
    1148239525157597184	RT @valeriasegoviat: Volvieron los Jonas Brothers, Hanna Montana, y todos odiamos a Justin Bieber de nuevo, estamos en el 2011. https://t.c…	1562590210	monoD-22	monicaba93	26526022	240619390
    1148239527804190720	Del mismo modo que no se necesitaba un hilo para demostrar lo mierda que es Justin Bieber, no se necesitaba un artí… https://t.co/s2rkqk90vN	1562590210	Alvaro Sin Acento	AlvaroRdzLpz	33984087	1246784260
    1148239514181283842	Y esos quienes son?? Prefiero ver el mundial de fútbol femenil  1562590210	Froggy	AbrahmGR	84992023	1251383680
    1148239567071453184	i’ve stanned selena on here literally since 2011 and i’ve seen it all. the death threats, racism, everything. just… https://t.co/ik0XFnukxb	1562590210	JEM	selenaftari	85031663	1259366400


## Test

To execute the tests run:
```
python -m unittest test_twitter.py
```