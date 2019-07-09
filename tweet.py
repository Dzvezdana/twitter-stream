import time

class Tweet(object):
    """
    A class representing the Tweet structure used by the Twitter API.
    
    Attributes
    ----------
    id : str
        tweet id
    text: str
        tweet text
    created_at : float
        tweet creation date
    username : str
        tweet author username
    user_screenname : str
        tweet author screename
    user_id: str
        tweet author user_id
    user_created_at: float
        creation date of the user profile

    Returns:
    ----------
        A Tweet Object
    """
    def __init__(self, data):
        self.id = data["id_str"]
        self.text = data["text"].strip()
        self.created_at = (time.mktime(time.strptime(data["created_at"], "%a %b %d %H:%M:%S +0000 %Y"))) # convert to epoch
        self.username = data["user"]["name"]
        self.user_screenname = data['user']['screen_name']
        self.user_id = data["user"]["id_str"]
        self.user_created_at = (time.mktime(time.strptime(data["user"]["created_at"], "%a %b %d %H:%M:%S +0000 %Y")))