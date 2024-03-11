from prometheus_client import start_http_server, Gauge
from googleapiclient.discovery import build
import os
import json
import time

# Define the scopes needed for the YouTube Data API
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

# Define metrics
gauge_metric_1 = Gauge('total_views', 'Total views on the channel', ['singer_name'])
gauge_metric_2 = Gauge('total_videos', 'Total videos on the channel', ['singer_name'])
gauge_metric_3 = Gauge('total_subscriber_count', 'Total subscriber count on the channel', ['singer_name'])

def get_channel_statistics(api_key, channel_id):
    """
    Retrieves channel statistics using the YouTube Data API.
    """
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.channels().list(
        part='statistics',
        id=channel_id
    )

    response = request.execute()

    if 'items' in response:
        for channel in response['items']:
            statistics = channel.get('statistics', {})
            return statistics
    else:
        print("No channel found.")
        return None

def generate_prometheus_values():
    """
    Periodically fetches channel statistics and updates Prometheus metrics.
    """
    while True:
        api_key = os.getenv("YOUTUBE_API_KEY","NULL")

        with open("./youtube_channels.json", 'r') as file:
            youtube_data = json.load(file)

        for channel in youtube_data:
            channel_id = channel["channel_id"]
            statistics = get_channel_statistics(api_key, channel_id)

            if statistics:
                singer_name = channel["channel_name"]
                total_views = int(statistics.get('viewCount', 0))
                total_videos = int(statistics.get('videoCount', 0))
                total_subscribers = int(statistics.get('subscriberCount', 0))

                # Update Prometheus metrics
                gauge_metric_1.labels(singer_name=singer_name).set(total_views)
                gauge_metric_2.labels(singer_name=singer_name).set(total_videos)
                gauge_metric_3.labels(singer_name=singer_name).set(total_subscribers)

        time.sleep(10)

if __name__ == '__main__':
    start_http_server(8000)
    generate_prometheus_values()
