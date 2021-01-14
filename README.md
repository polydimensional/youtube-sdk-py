# YoutubeSDK

Python SDK for accessing Youtube APIs.

## Installation

You can install it from pypi
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

# Quota
api_units = youtube.api_units_calculator(channel_id='UCp03YiAWc48Ay9Ew4Nu6_UA')

# Detailed statistics
channel_stats = youtube.get_channel_stats(channel_id='UCp03YiAWc48Ay9Ew4Nu6_UA')

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
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
