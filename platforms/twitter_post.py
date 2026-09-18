import logging
import os

import tweepy
from dotenv import load_dotenv

from platforms.base import SocialMedia

load_dotenv()

logger = logging.getLogger("Discord")


class Twitter(SocialMedia):
    def __init__(self, name, videoPath):
        super().__init__(name, videoPath)
        self.name = name
        self.videoPath = videoPath
        self.consumer_key = os.getenv("consumer_key")
        self.consumer_secret = os.getenv("consumer_secret_key")
        self.access_token = os.getenv("access_token")
        self.access_token_secret = os.getenv("access_token_secret")
        self.api = self.authenticate_conn_v1()
        self.client = self.authenticate_conn_v2()

    def authenticate_conn_v1(self):
        auth = tweepy.OAuth1UserHandler(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
        )
        api = tweepy.API(auth=auth)
        logger.info(f"Authorised V1: {api}")
        return api

    def authenticate_conn_v2(self):
        client = tweepy.Client(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
        )
        logger.info(f"Authorised V2: {client}")
        return client

    def post(self, message: list[str] | None = None, includeVideo=False) -> bool:
        if includeVideo:
            self.upload_media()

        message.append("-# uploaded w/ devlogs, my own custom discord bot.")
        message = "\n".join(message)
        response = self.client.create_tweet(text=message, media_ids=[self.media_id])
        return response

    def upload_media(self):
        with open(self.videoPath, "rb") as fp:
            self.media = self.api.media_upload(
                filename="devlog_video",
                file=fp,
                chunked=True,
                media_category="tweet_video",
            )
            self.media_id = self.media.media_id
