import json
import math

from . import constants

import requests


class Connection(object):
    """
    Parameters:
        api_key (str): The API key which is created from Google Cloud Console.

    Example usage:
        To create an instance of youtubesdk.Api class:
            >>> import youtubesdk
            >>> youtube = youtubesdk.Connection(api_key='your api key')
        To get one channel info:
            >>> response = youtube.get_channel_stats(channel_id='UCp03YiAWc48Ay9Ew4Nu6_UA')
            >>> print(response)
        Few other methods:
            >>> youtube.get_channel_info(channel_id='UCp03YiAWc48Ay9Ew4Nu6_UA')
            >>> youtube.get_video_by_id(video_id='rbfOxR3OiW8')
    """

    def __init__(self, api_key: str):
        self.api_key = api_key

        self.combined_search_ids = []
        self.combined_video_info = []
        self.api_units = 0


    def _get_request(self, endpoint, params, cost):
        self.api_units = self.api_units + cost
        print('units used till now is ', self.api_units)

        params['key'] = self.api_key
        params['maxResults'] = constants.MAX_RESULTS

        response = requests.get(endpoint, params)
        return json.loads(response.text)


    def _search(self, channel_id: str, page_token: str=None):
        api_params = {
            'part': constants.SEARCH_PARTS,
            'channelId': channel_id,
            'order': 'viewCount',
            'type': 'video',
            'pageToken': page_token
        }

        search_info = self._get_request('{0}/search'.format(constants.BASE_URL), api_params, 100)
        for item in search_info['items']:
            self.combined_search_ids.append(item['id']['videoId'])

        if 'nextPageToken' in search_info:
            self._search(channel_id=channel_id, page_token=search_info['nextPageToken'])
        else:
            return self.combined_search_ids


    def _get_videos_info(self, grouped_ids: list):
        for grouped_id in grouped_ids:
            video_info = self.get_video_by_id(video_id=grouped_id)
            self.combined_video_info.extend(video_info['items'])

        return self.combined_video_info


    def _group_data(self, videos_info, channel_info):
        most_viewed_video = videos_info[0]
        least_viewed_video = videos_info[len(videos_info) - 1]

        most_liked = int(videos_info[0]['statistics']['likeCount'])
        most_liked_video = {}
        most_disliked = int(videos_info[0]['statistics']['dislikeCount'])
        most_disliked_video = {}
        most_comment = int(videos_info[0]['statistics']['commentCount'])
        most_comments_video = {}

        least_liked = int(videos_info[0]['statistics']['likeCount'])
        least_liked_video = {}
        least_disliked = int(videos_info[0]['statistics']['dislikeCount'])
        least_disliked_video = {}
        least_comment = int(videos_info[0]['statistics']['commentCount'])
        least_comments_video = {}


        for item in videos_info:
            most_liked_count = int(item['statistics']['likeCount'])
            if most_liked_count >= most_liked:
                most_liked = most_liked_count
                most_liked_video = item

            most_disliked_count = int(item['statistics']['dislikeCount'])
            if most_disliked_count >= most_disliked:
                most_disliked = most_disliked_count
                most_disliked_video = item

            most_comment_count = int(item['statistics']['commentCount'])
            if most_comment_count >= most_comment:
                most_comment = most_comment_count
                most_comments_video = item


            least_liked_count = int(item['statistics']['likeCount'])
            if least_liked_count <= least_liked:
                least_liked = least_liked_count
                least_liked_video = item

            least_disliked_count = int(item['statistics']['dislikeCount'])
            if least_disliked_count <= least_disliked:
                least_disliked = least_disliked_count
                least_disliked_video = item

            least_comment_count = int(item['statistics']['commentCount'])
            if least_comment_count <= least_comment:
                least_comment = least_comment_count
                least_comments_video = item

        sentence = ' with count of '

        data = {
            'apiUnitsConsumed': self.api_units,
            'channelInfo': channel_info['items'][0],
            'lessVideosStats': {
                'most': {
                    'views': '{0}{1}{2}'.format(most_viewed_video['snippet']['title'], \
                        videos_info[0]['statistics']['viewCount'], sentence),
                    'likes': '{0}{1}{2}'.format(most_liked_video['snippet']['title'], most_liked, sentence),
                    'dislikes': '{0}{1}{2}'.format(most_disliked_video['snippet']['title'], most_disliked, sentence),
                    'comments': '{0}{1}{2}'.format(most_comments_video['snippet']['title'], most_comment, sentence)
                },
                'least': {
                    'views': '{0}{1}{2}'.format(least_viewed_video['snippet']['title'], \
                        videos_info[len(videos_info) - 1]['statistics']['viewCount'], sentence),
                    'likes': '{0}{1}{2}'.format(least_liked_video['snippet']['title'], most_liked, sentence),
                    'dislikes': '{0}{1}{2}'.format(least_disliked_video['snippet']['title'], most_disliked, sentence),
                    'comments': '{0}{1}{2}'.format(least_comments_video['snippet']['title'], most_comment, sentence)
                }
            },
            'detailedVideosStats': {
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

        return data


    def api_units_calculator(self, channel_id: str):
        """Get api units required for get_channel_stats().

        Parameters:
            channel_id (str): Channel ID.

        Note:
            Call to this method costs 1 api unit.

        Returns:
            Dict with api units count.
        """

        video_count = int(self.get_channel_info(channel_id=channel_id)['items'][0]['statistics']['videoCount'])
        split_call = math.ceil(video_count / 50)
        units = {
            'units': 1 + (split_call * 100) + split_call
        }

        return units


    def get_channel_info(self, channel_id: str):
        """Get channel info.

        Parameters:
            channel_id (str): Channel ID.

        Note:
            Call to this method costs 1 api unit.

        Returns:
            Dict with Channel info.
        """

        api_params = {
            'id': channel_id,
            'part': constants.CHANNELS_PART
        }

        return self._get_request('{0}/channels'.format(constants.BASE_URL), api_params, 1)


    def get_video_by_id(self, video_id: str):
        """Get video info.

        Parameters:
            video_id (str): Video ID.

        Note:
            Call to this method costs 1 api unit.

        Returns:
            Dict with Video info.
        """

        api_params = {
            'part': constants.VIDEOS_PART,
            'id': video_id
        }

        return self._get_request('{0}/videos'.format(constants.BASE_URL), api_params, 1)


    def get_channel_stats(self, channel_id: str):
        """Get channel detailed statistics.

        Parameters:
            channel_id (str): Channel ID.

        Note:
            Call to this method costs api units based on channel size.
            Call to api_units_calculator() to get api units calculation.

        Returns:
            Dict with Channel and Video Statistics.
        """

        channel_info = self.get_channel_info(channel_id=channel_id)
        self._search(channel_id=channel_id)

        group_ids = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
        grouped_ids = group_ids(self.combined_search_ids, int(constants.MAX_RESULTS))
        videos_info = self._get_videos_info(grouped_ids)

        return self._group_data(videos_info, channel_info)