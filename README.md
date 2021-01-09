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
channel = youtube.get_channel_info(channel_id='UCjCyBDj910msVKhchKNl_sA')

# Quota
api_units = youtube.api_units_calculator(channel_id='UCjCyBDj910msVKhchKNl_sA')

# Detailed statistics
channel_stats = youtube.get_channel_stats(channel_id='UCjCyBDj910msVKhchKNl_sA')

# Video
video = youtube.get_video_by_id(video_id='fIU92IzgEfU')
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
