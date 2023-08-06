aiobotocore
===========
.. image:: https://travis-ci.org/aio-libs/aiobotocore.svg?branch=master
    :target: https://travis-ci.org/aio-libs/aiobotocore
.. image:: https://codecov.io/gh/aio-libs/aiobotocore/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/aio-libs/aiobotocore
.. image:: https://img.shields.io/pypi/v/aiobotocore.svg
    :target: https://pypi.python.org/pypi/aiobotocore

Async client for amazon services using botocore_ and aiohttp_/asyncio_.

Main purpose of this library to support amazon s3 api, but other services
should work (may be with minor fixes). For now we have tested
only upload/download api for s3, other users report that SQS and Dynamo
services work also. More tests coming soon.


Install
-------
::

    $ pip install aiobotocore


Basic Example
-------------

.. code:: python

    import asyncio
    import aiobotocore

    AWS_ACCESS_KEY_ID = "xxx"
    AWS_SECRET_ACCESS_KEY = "xxx"


    async def go(loop):
        bucket = 'dataintake'
        filename = 'dummy.bin'
        folder = 'aiobotocore'
        key = '{}/{}'.format(folder, filename)

        session = aiobotocore.get_session(loop=loop)
        async with session.create_client('s3', region_name='us-west-2',
                                       aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                       aws_access_key_id=AWS_ACCESS_KEY_ID) as client:
            # upload object to amazon s3
            data = b'\x01'*1024
            resp = await client.put_object(Bucket=bucket,
                                                Key=key,
                                                Body=data)
            print(resp)

            # getting s3 object properties of file we just uploaded
            resp = await client.get_object_acl(Bucket=bucket, Key=key)
            print(resp)

            # delete object from s3
            resp = await client.delete_object(Bucket=bucket, Key=key)
            print(resp)

            # list s3 objects using paginator
            paginator = client.get_paginator('list_objects')
            async for result in paginator.paginate(Bucket=bucket, Prefix=folder):
                for c in result.get('Contents', []):
                    print(c)

            # get object from s3
            response = await client.get_object(Bucket=bucket, key=key)
            # this will ensure the connection is correctly re-used/closed
            async with response['Body'] as stream:
                data = await stream.read()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(go(loop))


Run Tests
---------

Make sure you have development requirements installed and your amazon key and
secret accessible via environment variables:

::

    $ cd aiobotocore
    $ export AWS_ACCESS_KEY_ID=xxx
    $ export AWS_SECRET_ACCESS_KEY=xxx
    $ pip install -Ur requirements-dev.txt

Execute tests suite:

::

    $ py.test -v tests


Mailing List
------------

https://groups.google.com/forum/#!forum/aio-libs


Requirements
------------
* Python_ 3.4+
* aiohttp_
* botocore_

.. _Python: https://www.python.org
.. _asyncio: http://docs.python.org/3.4/library/asyncio.html
.. _botocore: https://github.com/boto/botocore
.. _aiohttp: https://github.com/KeepSafe/aiohttp

Changes
-------
0.3.1 (2017-04-18)
^^^^^^^^^^^^^^^^^^
* Fixed Waiter support

0.3.0 (2017-04-01)
^^^^^^^^^^^^^^^^^^
* Added support for aiohttp>=2.0.4 (thanks @achimnol)
* update botocore requirement to: botocore>=1.5.0, <=1.5.33

0.2.3 (2017-03-22)
^^^^^^^^^^^^^^^^^^
* update botocore requirement to: botocore>=1.5.0, <1.5.29

0.2.2 (2017-03-07)
^^^^^^^^^^^^^^^^^^
* set aiobotocore.__all__ for * imports #121 (thanks @graingert)
* fix ETag in head_object response #132

0.2.1 (2017-02-01)
^^^^^^^^^^^^^^^^^^
* Normalize headers and handle redirection by botocore #115 (thanks @Fedorof)

0.2.0 (2017-01-30)
^^^^^^^^^^^^^^^^^^
* add support for proxies (thanks @jjonek)
* remove AioConfig verify_ssl connector_arg as this is handled by the
  create_client verify param
* remove AioConfig limit connector_arg as this is now handled by
  by the Config `max_pool_connections` property (note default is 10)

0.1.1 (2017-01-16)
^^^^^^^^^^^^^^^^^^
* botocore updated to version 1.5.0

0.1.0 (2017-01-12)
^^^^^^^^^^^^^^^^^^
* Pass timeout to aiohttp.request to enforce read_timeout #86 (thanks @vharitonsky)
  (bumped up to next semantic version due to read_timeout enabling change)

0.0.6 (2016-11-19)
^^^^^^^^^^^^^^^^^^

* Added enforcement of plain response #57 (thanks @rymir)
* botocore updated to version 1.4.73 #74 (thanks @vas3k)


0.0.5 (2016-06-01)
^^^^^^^^^^^^^^^^^^

* Initial alpha release

