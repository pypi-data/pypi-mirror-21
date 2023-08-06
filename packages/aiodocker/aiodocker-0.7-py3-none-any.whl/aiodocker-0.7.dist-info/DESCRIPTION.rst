AsyncIO bindings for docker.io
==============================

|PyPI version| |Python Versions| |Build Status| |Code Coverage|

A simple Docker HTTP API wrapper written with asyncio and aiohttp.

Installation
------------

.. code:: sh

    pip install aiodocker

For development version:

.. code:: sh

    pip install 'git+https://github.com/aio-libs/aiodocker#egg=aiodocker'

Examples
--------

.. code:: python

    import asyncio
    import aiodocker

    async def list_things():
        docker = aiodocker.Docker()
        print('== Images ==')
        for image in (await docker.images.list()):
            print(f" {image['Id']} {image['RepoTags'][0] if image['RepoTags'] else ''}")
        print('== Containers ==')
        for container in (await docker.containers.list()):
            print(f" {container._id}")
        await docker.close()

    async def run_container():
        docker = aiodocker.Docker()
        print('== Running a hello-world container ==')
        container = await docker.containers.create_or_replace(
            config={
                'Cmd': ['/bin/ash', '-c', 'echo "hello world"'],
                'Image': 'alpine:latest',
            },
            name='testing',
        )
        await container.start()
        logs = await container.log(stdout=True)
        print(''.join(logs))
        await container.delete(force=True)
        await docker.close()

    if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(list_things())
        loop.run_until_complete(run_container())
        loop.close()

.. |PyPI version| image:: https://badge.fury.io/py/aiodocker.svg
   :target: https://badge.fury.io/py/aiodocker
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/aiodocker.svg
   :target: https://pypi.org/project/aiodocker/
.. |Build Status| image:: https://travis-ci.org/aio-libs/aiodocker.svg?branch=master
   :target: https://travis-ci.org/aio-libs/aiodocker
.. |Code Coverage| image:: https://codecov.io/gh/aio-libs/aiodocker/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/aio-libs/aiodocker


