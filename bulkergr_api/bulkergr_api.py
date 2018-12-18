# -*- coding: utf-8 -*-

import requests
import os.path
import logging
import sys
import time

from .exceptions import AuthKeyMissingError

SMS_URL = 'https://api.bulker.gr/http/sms.php/'
DLR_URL = 'https://api.bulker.gr/http/dlr.php/'
BALANCE_URL = 'https://api.bulker.gr/http/balance.php/'

logger = logging.getLogger('bulkergr')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stderr))


class Bulkergr(object):
    def __init__(self, auth_key=None, debug=False):
        """
        Initialize API Client
        :param auth_key: (str|None)
        """
        # setup auth_key
        if auth_key is None:
            if 'BULKERGR_AUTH_KEY' in os.environ:
                auth_key = os.environ['BULKERGR_AUTH_KEY']
            else:
                raise AuthKeyMissingError('You must provide an authorization key.')
        self.auth_key = auth_key
        # setup global session
        self.session = requests.session()
        # setup debug level
        if debug:
            self.level = logging.INFO
        else:
            self.level = logging.DEBUG

    def submit_sms(self, params):
        """
        Submit sms for sending
        :param params: dict with bulkergr API's format
        :return: requests instance response
        """
        return self.post(SMS_URL, params)

    def post(self, url, params=None):
        """
        Make an actual post request to bulker.gr endpoint.
        :param url: str
        :param params: dict
        :return: requests instance response
        """
        # pass auth_key
        if params is None:
            params = {}
        params['auth_key'] = self.auth_key
        # pass sms id
        if 'id' not in params or params['id'] is None:
            params['id'] = self.generate_unique_id()
        # log POST try
        self.log('POST to %s: %s' % (url, params))
        response = self.session.post(url, data=params, headers={'user-agent': 'Bulkergr-API-Client/0.1.4'})
        return self.parse_response_text(response)

    @staticmethod
    def generate_unique_id():
        """
        Every request in bulker.gr requires an unique integer per SMS as id.
        When this id is not generated through an autoincrement key value from
        a DB table, alternatively we can send back the current timestamp
        in milliseconds.
        :return: current timestamp in milliseconds
        """
        return int(round(time.time() * 1000))

    @staticmethod
    def parse_response_text(response):
        """
        Bulkergr API returns text in CVS format so we need to parse
        and convert it to a dictionary so we can easily access it
        :param response: enhanced requests instance response
        :return:
        """
        response.results = dict()
        response.results['ACK'] = response.text.split(';')[0]
        response.results['id'] = response.text.split(';')[1]
        response.results['charge'] = response.text.split(';')[2]
        # check if its an actual error or OK
        if response.results['ACK'].startswith('ERROR'):
            response.results['error'] = True
        else:
            response.results['error'] = False
        return response

    def log(self, *args, **kwargs):
        logger.log(self.level, *args, **kwargs)

    def __repr__(self):
        return '<Bulker.gr %s>' % self.auth_key
