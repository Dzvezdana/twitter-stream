FROM adoptopenjdk/openjdk8

RUN apt-get update \
    && apt-get install -y python3 python3-dev python3-pip python3-virtualenv \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get install -y --no-install-recommends curl ca-certificates locales \
    && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install requests pyspark oauth2

ADD twitter_stream.py /
ADD tweet.py /

# Add keys here
ENV TWITTER_API_KEY=""
ENV TWITTER_API_SECRET=""
ENV TWITTER_ACCESS_TOKEN=""
ENV TWITTER_ACCESS_TOKEN_SECRET=""

RUN ln -s /usr/bin/python3 /usr/bin/python

CMD [ "python3", "/twitter_stream.py" ]