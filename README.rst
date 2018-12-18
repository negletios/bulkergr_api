===========================
A Python API Client for https://www.bulker.gr
===========================


.. image:: https://img.shields.io/pypi/v/bulkergr_api.svg
        :target: https://pypi.python.org/pypi/bulkergr_api

.. image:: https://readthedocs.org/projects/bulkergr-api/badge/?version=latest
        :target: https://bulkergr-api.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/negletios/bulkergr_api/shield.svg
     :target: https://pyup.io/repos/github/negletios/bulkergr_api/
     :alt: Updates



A Python Client for v1.0 of Bulker.gr SMS HTTP API


* Free software: MIT license
* Documentation: https://bulkergr-api.readthedocs.io.

Installation
------------

``pip install bulkergr-api``

Examples
--------

Submit a simple SMS through bulker.gr API SMS HTTP Client.

.. code-block:: python

    from bulkergr_api import Bulkergr

    AUTH_KEY = 'XXXX'  # your auth key here.

    bulker = Bulkergr(auth_key=AUTH_KEY)
    params = {
        'from': 'XXXX',  # from sender parameter depending on your bulker.gr account
        'to': 'XXXXX',  # mobile number (MSISDN), starting with country code
        'text': 'some random text here',
    }

    r = bulker.submit_sms(params)
    print(r.results)

Features
--------

* Submit SMS to the API
* Converting CSV text response to dict

TODO
--------

* Integrate delivery receipts
* Integrate balance queries
* Enhance library's features of submitting
* Enhance library's validity checks
* Complete tests based on API
* Write the docs
* Enable cli functionality

Compatibility
-------------

python2.7
python3.4+

Credits
-------

This package was created with :heart: by negletios_.

.. _negletios: https://github.com/negletios/
