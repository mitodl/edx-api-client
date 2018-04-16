"""A wrapper in requester"""
import requests


class Requester(object):
    """A wrapper in requester"""

    def __init__(self, timeout, access_token):
        """
        Args:
            timeout (number or tuple): How long to wait for the server to send
                data before giving up, as a float, or a :ref:`(connect timeout,
                read timeout) <timeouts>` tuple.
            access_token (str): access token for edx apis
        """
        self.timeout = timeout
        # generating an EdxApi instance with the proper requester & credentials.
        self.session = requests.session()
        self.session.headers.update({
            'Authorization': 'Bearer {}'.format(access_token)
        })

    def get(self, url, **kwargs):
        """
        Wrapper for requests get call.

        Args:
            url (str): edX api url
            kwargs (dict): other params
        """
        return self.session.get(url, timeout=self.timeout, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        """
        Wrapper for requests post call.

        Args:
            url (str): edX api url
            data (dict): payload of query params
            json (json): json payload
            kwargs (dict): other params
        """
        return self.session.post(
            url,
            data=data,
            json=json,
            timeout=self.timeout,
            **kwargs
        )

    def options(self, url, **kwargs):
        """
        Wrapper for requests options call.
        Args:
            url (str): url of edx api
            kwargs (dict): other params
        """
        return self.session.options(url, timeout=self.timeout, **kwargs)

    def head(self, url, **kwargs):
        """
        Wrapper for requests head call.
        Args:
            url (str): url of edx api
           kwargs (dict): other params
        """
        return self.session.head(url, timeout=self.timeout, **kwargs)

    def put(self, url, data=None, **kwargs):
        """
        Wrapper for requests put call.
        Args:
            url (str): url of edx api
            data (dict): payload of query params
            kwargs (dict): other params
        """
        return self.session.put(url, data=data, timeout=self.timeout, **kwargs)

    def patch(self, url, data=None, **kwargs):
        """
        Wrapper for requests patch call.
        Args:
            url (str): url of edx api
            data (dict): payload of query params
            kwargs (dict): other params
        """
        return self.session.patch(url, data=data, timeout=self.timeout, **kwargs)

    def delete(self, url, **kwargs):
        """
        Wrapper for requests delete call.
        Args:
            url (str): url of edx api
            kwargs (dict): other params
        """
        return self.session.delete(url, timeout=self.timeout, **kwargs)
