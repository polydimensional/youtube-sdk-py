import json
import math

from . import constants
from .exceptions import InvalidKeyError, MissingParamsError, WrongParamsError

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
            >>> youtube.get_channel(channel_id='UCp03YiAWc48Ay9Ew4Nu6_UA')
            >>> youtube.get_video(video_id='rbfOxR3OiW8')
            >>> youtube.api_units_calculator(channel_id='UCp03YiAWc48Ay9Ew4Nu6_UA')
            >>> print(youtube.api_units)
            >>> youtube.get_comment_threads(video_id='EkDuCWOHBVU')
            >>> youtube.get_comments(comment_id='UgwNpeGtLn59UjTrW7N4AaABAg')
            >>> youtube.get_playlist_items(playlist_id='PL9a4goxNJut0xjwPV4CZlIJUGuOzwrih0')
            >>> youtube.get_playlists(playlist_id='PL9a4goxNJut0xjwPV4CZlIJUGuOzwrih0')
            >>> youtube.get_search(channel_id='UCp03YiAWc48Ay9Ew4Nu6_UA', query='full stack')
    """

    def __init__(self, api_key: str):
        self.api_key = api_key

        self.combined_search_ids = []
        self.combined_video_info = []
        self._api_units = 0


    def _get_request(self, endpoint: str, params: dict, cost: int, page_token:str = None):
        self._api_units = self._api_units + cost

        params['key'] = self.api_key
        params['maxResults'] = constants.MAX_RESULTS
        params['pageToken'] = page_token

        response = requests.get(endpoint, params)
        loaded_response = json.loads(response.text)

        if response.status_code == 200:
            if 'error' in loaded_response and loaded_response['error']:
                raise WrongParamsError('Some error has occured', loaded_response)

            elif not loaded_response['items']:
                raise WrongParamsError('Item not found', loaded_response)

            else:
                return loaded_response

        elif response.status_code == 400:
            if 'API key not valid' in loaded_response['error']['message']:
                raise InvalidKeyError('API key not valid', loaded_response)
            else:
                raise WrongParamsError('Unknown error has occured', loaded_response)

        else:
            raise WrongParamsError('Unknown error has occured', loaded_response)


    def _search(self, channel_id: str, page_token: str=None):
        search_info = self.get_search(channel_id=channel_id, order='viewCount', type='video', page_token=page_token)
        for item in search_info['items']:
            self.combined_search_ids.append(item['id']['videoId'])

        if 'nextPageToken' in search_info:
            self._search(channel_id=channel_id, page_token=search_info['nextPageToken'])
        else:
            return self.combined_search_ids


    def _get_videos_info(self, grouped_ids: list):
        for grouped_id in grouped_ids:
            video_info = self.get_video(video_id=grouped_id)
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

        data = {
            'apiUnitsConsumed': self._api_units,
            'channelInfo': channel_info['items'][0],
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

        if not channel_id:
            raise MissingParamsError(message='channel_id is required')

        video_count = int(self.get_channel(channel_id=channel_id)['items'][0]['statistics']['videoCount'])
        split_call = math.ceil(video_count / 50)
        units = {
            'units': 1 + (split_call * 100) + split_call
        }

        return units


    def get_channel(self, channel_id: str=None, user_name: str=None, page_token: str=None):
        """Get channel info.

        Parameters:
            channel_id (str): Channel ID.

        Note:
            Call to this method costs 1 api unit.

        Returns:
            Dict with Channel info.
        """

        if not channel_id and not user_name:
            raise MissingParamsError(message='channel_id or user_name is required')

        api_params = {
            'id': channel_id,
            'forUsername': user_name if not channel_id else None,
            'part': constants.CHANNELS_PART
        }

        return self._get_request('{0}/channels'.format(constants.BASE_URL), api_params, 1, page_token)


    def get_video(self, video_id: str, page_token: str=None):
        """Get video info.

        Parameters:
            video_id (str): Video ID.

        Note:
            Call to this method costs 1 api unit.

        Returns:
            Dict with Video info.
        """

        if not video_id:
            raise MissingParamsError(message='video_id is required')

        api_params = {
            'part': constants.VIDEOS_PART,
            'id': video_id
        }

        return self._get_request('{0}/videos'.format(constants.BASE_URL), api_params, 1, page_token)


    def get_comment_threads(self, video_id: str=None, channel_id: str=None, comment_id: str=None, page_token: str=None):
        """Get comments info.

        Parameters:
            video_id (str): Video ID.
            channel_id (str): Channel ID.
            comment_id (str): Comment ID.

        Note:
            Call to this method costs 1 api unit.

        Returns:
            Dict with Comment Threads info.
        """

        if not video_id and not channel_id and not comment_id:
            raise MissingParamsError(message='video_id or channel_id or comment_id is required')

        api_params = {
            'part': constants.COMMENT_THREADS_PARTS
        }

        if comment_id:
            api_params['id'] = comment_id
        elif video_id:
            api_params['videoId'] = video_id
        elif channel_id:
            api_params['channelId'] = channel_id

        return self._get_request('{0}/commentThreads'.format(constants.BASE_URL), api_params, 1, page_token)


    def get_comments(self, comment_id: str, page_token: str=None):
        """Get comment info.

        Parameters:
            comment_id (str): Comment ID.

        Note:
            Call to this method costs 1 api unit.

        Returns:
            Dict with Comment info.
        """

        if not comment_id:
            raise MissingParamsError(message='comment_id is required')

        api_params = {
            'part': constants.COMMENTS_PARTS,
            'id': comment_id
        }

        return self._get_request('{0}/comments'.format(constants.BASE_URL), api_params, 1, page_token)


    def get_playlist_items(self, playlist_id: str=None, playlist_item_id: str=None, page_token: str=None):
        """Get playlist items info.

        Parameters:
            playlist_id (str): Playlist ID.
            playlist_item_id (str): Playlist Item ID.

        Note:
            Call to this method costs 1 api unit.

        Returns:
            Dict with Playlist items info.
        """

        if not playlist_id and not playlist_item_id:
            raise MissingParamsError(message='playlist_id or playlist_item_id is required')

        api_params = {
            'playlistId': playlist_id,
            'id': playlist_item_id if not playlist_id else None,
            'part': constants.PLAYLIST_ITEMS_PARTS
        }

        return self._get_request('{0}/playlistItems'.format(constants.BASE_URL), api_params, 1, page_token)


    def get_playlists(self, playlist_id: str=None, channel_id: str=None, page_token: str=None):
        """Get playlist items info.

        Parameters:
            playlist_id (str): Playlist ID.
            channel_id (str): Channel ID.

        Note:
            Call to this method costs 1 api unit.

        Returns:
            Dict with Playlist item info.
        """

        if not playlist_id and not channel_id:
            raise MissingParamsError(message='playlist_id or channel_id is required')

        api_params = {
            'id': playlist_id,
            'channelId': channel_id if not playlist_id else None,
            'part': constants.PLAYLISTS_PARTS
        }

        return self._get_request('{0}/playlists'.format(constants.BASE_URL), api_params, 1, page_token)


    def get_search(self, channel_id: str=None, channel_type: str=None, event_type: str=None,
                    location: str=None, location_radius: str=None, order: str='viewCount',
                    query: str=None, region_code: str=None, safe_search: str=None,
                    topic_id: str=None,video_type: str=None, page_token: str=None, **kwargs):
        """Get search.

        Parameters:
            playlist_id (str): Playlist ID.
            channel_id (str): Channel ID.
            channel_type (str): Channel Type.
            event_type (str): Event Type.
            location (str): Location.
            location_radius (str): Location Radius.
            order (str): Order.
            query (str): Query.
            region_code (str): Region Code.
            safe_search (str): Safe Search.
            topic_id (str): Topic ID.
            video_type (str): Video Type.
            page_token (str): Page Token.
            **kwargs - any other params that youtube search api accepts

        Note:
            Call to this method costs 100 api unit.

        Returns:
            Dict with Search info.
        """

        api_params = {
            'part': constants.SEARCH_PARTS,
            'channelId': channel_id,
            'channelType': channel_type,
            'eventType': event_type,
            'location': location,
            'locationRadius': location_radius,
            'order': order,
            'q': query,
            'regionCode': region_code,
            'safeSearch': safe_search,
            'topicId': topic_id,
            'type': video_type,
            **kwargs
        }

        return self._get_request('{0}/search'.format(constants.BASE_URL), api_params, 100, page_token)


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

        if not channel_id:
            raise MissingParamsError(message='channel_id is required')

        channel_info = self.get_channel(channel_id=channel_id)
        self._search(channel_id=channel_id)

        group_ids = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
        grouped_ids = group_ids(self.combined_search_ids, int(constants.MAX_RESULTS))
        videos_info = self._get_videos_info(grouped_ids)

        if videos_info and channel_info:
            return self._group_data(videos_info, channel_info)
        else:
            return {'apiUnitsConsumed': self._api_units, 'error': 'Sufficient amount of data not found'}


    @property
    def api_units(self):
        """
        Get the api_units
        """
        return self._api_units
