import youtubesdk

youtube = youtubesdk.Connection(api_key='your api key')

channel = youtube.get_channel_info(channel_id='UCjCyBDj910msVKhchKNl_sA')
print('channel response:', channel)

api_units = youtube.api_units_calculator(channel_id='UCjCyBDj910msVKhchKNl_sA')
print('api_units response:', api_units)

channel_stats = youtube.get_channel_stats(channel_id='UCjCyBDj910msVKhchKNl_sA')
print('channel_stats response:', channel_stats)

video = youtube.get_video_by_id(video_id='fIU92IzgEfU')
print('video:', video)
