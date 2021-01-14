import youtubesdk
from youtubesdk import InvalidKeyError, MissingParamsError, WrongParamsError

youtube = youtubesdk.Connection(api_key='your api key')

try:
    channel = youtube.get_channel(channel_id='UCp03YiAWc48Ay9Ew4Nu6_UA')
    print('channel response:', channel)

    api_units = youtube.api_units_calculator(channel_id='UCp03YiAWc48Ay9Ew4Nu6_UA')
    print('api_units response:', api_units)

    channel_stats = youtube.get_channel_stats(channel_id='UCp03YiAWc48Ay9Ew4Nu6_UA')
    print('channel_stats response:', channel_stats)

    video = youtube.get_video(video_id='rbfOxR3OiW8')
    print('video:', video)

    comment_thread = youtube.get_comment_threads(video_id='EkDuCWOHBVU')
    print('comment_thread:', comment_thread)

    comments = youtube.get_comments(comment_id='UgwNpeGtLn59UjTrW7N4AaABAg')
    print('comments:', comments)

    playlist_items = youtube.get_playlist_items(playlist_id='PL9a4goxNJut0xjwPV4CZlIJUGuOzwrih0')
    print('playlist_items:', playlist_items)

    playlists = youtube.get_playlists(channel_id='UCp03YiAWc48Ay9Ew4Nu6_UA')
    print('playlists:', playlists)

    search = youtube.get_search(channel_id='UCp03YiAWc48Ay9Ew4Nu6_UA', query='full stack')
    print('search:', search)

except InvalidKeyError as error:
    print('InvalidKeyError:', error, error.__dict__)

except MissingParamsError as error:
    print('MissingParamsError:', error, error.__dict__)

except WrongParamsError as error:
    print('WrongParamsError:', error, error.__dict__)

except Exception as error:
    print('Exception:', error, error.__dict__)
