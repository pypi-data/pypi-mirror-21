"""
Copyright (c) 2016-2017 Levi Sabah <x@levisabah.com> (https://github.com/levisabah/we-get/)
See the file 'LICENSE' for copying.
"""

import urllib.request
import urllib.parse
import urllib.error
from we_get.core.utils import random_user_agent
from we_get.core.utils import msg_error
from html import unescape as html_decode

USER_AGENT = random_user_agent()

class Module(object):
    def __init__(self):
        self.cursor = None

    def http_get_request(self, url):
        """ http_request: create HTTP request.
	        @return: data.
        """
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', USER_AGENT), ("Accept", "*/*")]
        try:
            return opener.open(url).read().decode()
        except urllib.error.URLError:
            msg_error("connection failed (%s)" % (url), True)

    def http_custom_get_request(self, url, headers):
        """ http_custom_get_request: HTTP GET request with custom headers. 
            @return: data.
        """
        opener = urllib.request.build_opener()
        opener.addheaders = headers
        return opener.open(url).read()

    def magnet2name(self, link):
        """ magnet2name: return torrent name from magnet link.
            @param magnet: link.
        """
        return link.split("&")[1].split("dn=")[1]

    def fix_name(self, name):
        """ fix_name: fix the torrent_name (Hello%20%20Worl+d to Hello_World).
            @parma name: torrent_name
        """
        name = html_decode(name)
        return urllib.parse.unquote(name.replace('+', '.')
            .replace('[', '')
            .replace(']', '')
            .replace(' ', '.')
            .replace('\'', ''))
