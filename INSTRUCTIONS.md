# README #

Please read the following instructions carefully and make sure that you fulfill all the requirements listed.

## Task ##

We would like you to write code that will cover the functionality listed below and provide us with the source as well as the output of an execution:

+ Connect to the [Twitter Streaming API](https://developer.twitter.com/en/docs/tutorials/consuming-streaming-data)
+ Filter messages that track on "bieber"
+ Retrieve the incoming messages for 30 seconds or up to 100 messages, whichever comes first
+ For each message, we will need the following:
	* The message ID
	* The creation date of the message as epoch value
	* The text of the message
	* The author of the message
+ For each author, we will need the following:
	* The user ID
	* The creation date of the user as epoch value
	* The name of the user
	* The screen name of the user
+ Your application should return the messages grouped by user (users sorted chronologically, ascending)
+ The messages per user should also be sorted chronologically, ascending
+ Print this information to a tab-separated file, with the a header containing the column names

## Notes ##

Please, create your own modules, and **do not use off-the-shelf libraries** to interact with Twitter. You can, of course, use available or native HTTP/RESTful API modules.
You will need to provide the _Consumer Key_ and _Consumer Secret_ and follow through the OAuth process (get temporary token, retrieve access URL, authorise application, enter PIN for authenticated token). You can find more information how-to [here](https://developer.twitter.com/en/docs/basics/authentication/overview/application-only)
