#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `bulkergr_api` package."""

import vcr

from bulkergr_api import Bulkergr
from bulkergr_api import AuthKeyMissingError

# TEST DATA
AUTH_KEY = '#######'  # add your API key
SMS_TO = '#######'  # add a test number that you receive
SMS_FROM = '#######'  # add a test sender
SMS_TEXT = 'test messages here'
SMS_ID = '12312311231331'
SMS_NOT_UNIQUE_ID = '3123123123131'  # id from previous submission


def test_initialization_without_auth_key():
    try:
        Bulkergr()
        assert False
    except AuthKeyMissingError:
        assert True


def bulkergr_submit_message(sms_id=None, sms_from=SMS_FROM, sms_to=SMS_TO, sms_text=SMS_TEXT):
    """
    Test common function that sends an sms message
    and return the bulker's response
    :return: bulker instance response
    """
    bulker = Bulkergr(auth_key=AUTH_KEY)
    params = dict()
    params['from'] = sms_from
    params['to'] = sms_to
    params['text'] = sms_text
    if sms_id is not None:
        params['id'] = sms_id
    return bulker.submit_sms(params)


@vcr.use_cassette('tests/vcr_cassettes/test_success_submit_message.yml')
def test_success_submit_message():
    response = bulkergr_submit_message()
    assert isinstance(response.results, dict)
    assert response.results['ACK'] == 'OK'


@vcr.use_cassette('tests/vcr_cassettes/test_success_submit_message_with_id.yml')
def test_success_submit_message_with_id():
    response = bulkergr_submit_message(sms_id=SMS_ID)
    assert isinstance(response.results, dict)
    assert response.results['ACK'] == 'OK'
    assert response.results['id'] == SMS_ID
    assert response.results['error'] is False


@vcr.use_cassette('tests/vcr_cassettes/test_error_submit_message_same_id.yml')
def test_error_submit_message_same_id():
    response = bulkergr_submit_message(sms_id=SMS_NOT_UNIQUE_ID)
    assert isinstance(response.results, dict)
    assert response.results['ACK'] == 'ERROR: id is already used.'
    response.results['error'] is True

