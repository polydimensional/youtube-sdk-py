# YoutubeSDK

Python SDK for accessing Youtube APIs.


## Requirements

* Python 3
* Requests library

`$ pip install requests`

## Installation

Install from pip

`$ pip install youtube-sdk-py`

## Usage

You can just initialize with an api key:
```python
import youtubesdk

youtube = youtubesdk.Connection(api_key='your api key')
```

Access various methods in this format
```python
# Channel
channel = youtube.get_channel(channel_id='UCp03YiAWc48Ay9Ew4Nu6_UA')

# Video
video = youtube.get_video(video_id='rbfOxR3OiW8')

# Comment Threads
comment_threads = youtube.get_comment_threads(video_id='EkDuCWOHBVU')

# Comments
comments = youtube.get_comments(comment_id='UgwNpeGtLn59UjTrW7N4AaABAg')

# Playlist Items
playlist_items = youtube.get_playlist_items(playlist_id='PL9a4goxNJut0xjwPV4CZlIJUGuOzwrih0')

# Playlists
playlists = youtube.get_playlists(channel_id='UCp03YiAWc48Ay9Ew4Nu6_UA')

# Search
search = youtube.get_search(channel_id='UCp03YiAWc48Ay9Ew4Nu6_UA', query='full stack')

# Quota
api_units = youtube.api_units_calculator(channel_id='UCp03YiAWc48Ay9Ew4Nu6_UA')

# Channel Statistics - This would return data in the below schema
channel_stats = youtube.get_channel_stats(channel_id='UCp03YiAWc48Ay9Ew4Nu6_UA')
{
    'apiUnitsConsumed': api_units,
    'channelInfo': channel_info,
    'detailedVideoStats': {
        'most': {
            'views': most_viewed_video,
            'likes': most_liked_video,
            'dislikes': most_disliked_video,
            'comments': most_comments_video
        },
        'least': {
            'views': least_viewed_video,
            'likes': least_liked_video,
            'dislikes': least_disliked_video,
            'comments': least_comments_video
        }
    }
}

```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
