# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import logging
import googleapiclient.discovery
import googleapiclient.errors


logging.basicConfig()

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def get_video_details(video_id):
    """
    calling YouTube API to return some details about the video

    Args:
        video_id: str

    Returns:
        video_title: str or None
        thumbnail_url: str or None
    """
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=os.environ["YOUTUBE_API_KEY"])

    request = youtube.videos().list(
        part=["contentDetails", "snippet"],
        id=video_id
    )
    try:
        response = request.execute()
        snippet = response["items"][0]["snippet"]
        video_title = snippet["title"]
        thumbnail_url = snippet["thumbnails"]["standard"]["url"]
        logging.debug("video title is: {} and thumbnail is {}".format(video_title, thumbnail_url))
    except KeyError as error:
        logging.debug(error)
        video_title = None
        thumbnail_url = None

    return video_title, thumbnail_url


if __name__ == "__main__":
    get_video_details("0Vbj9xFgoUw")
