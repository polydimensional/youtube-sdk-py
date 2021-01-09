
class YoutubeSDKError(Exception):

    def __init__(self, message=None, response=None):
        super(YoutubeSDKError, self).__init__(message)
        self.message = message
        self.response = response

    def __str__(self):
        return repr(self.message)


class InvalidKeyError(YoutubeSDKError):
    """Invalid api key"""
    pass


class MissingParamsError(YoutubeSDKError):
    """Some of the parameters in the request are missing."""
    pass


class WrongParamsError(YoutubeSDKError):
    """Some of the parameters in the request are wrong."""
    pass
