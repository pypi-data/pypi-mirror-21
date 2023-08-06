takumi-http
===========

.. image:: https://travis-ci.org/elemepi/takumi-http.svg?branch=master
    :target: https://travis-ci.org/elemepi/takumi-http


Use http client to call thrift services.


Example
-------

App config:

.. code:: yaml

    # app.yaml
    app_name: http_app
    port: 1991
    app: http_app:app
    thrift_file: ping.thrift
    thrift_protocol_class: takumi_http.protocol.HttpProtocol


App code:

.. code:: python

    # http_app.py

    from takumi import Takumi

    app = Takumi('PingService')

    @app.api
    def ping():
        return 'pong'


Start the service using `takumi-cli <https://github.com/elemepi/takumi-cli>`_.

.. code:: bash

    $ takumi serve


Then open http://localhost:1991/ping in your brower.
