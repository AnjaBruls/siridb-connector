SiriDB - Connector
==================

This manual describes how to install and configure SiriDB Connector for Python 3, a self-contained Python driver for communicating with SiriDB servers, and how to use it to develop database applications.


---------------------------------------
  * [Installation](#installation)
  * [Quick usage](#quick-usage)
  * [SiriDBClient](#siridbclient)
    * [connect](#siridbclientconnect)
    * [insert](#siridbclientinsert)
    * [query](#siridbclientquery)
    * [close](#siridbclientclose)
  * [Exception codes](#exception-codes)
  * [Version info](#version-info)

---------------------------------------

## Installation
------------

From PyPI (recommend)

```
pip install siridb-connector
```

From source code

```
python setup.py install
```


## Quick usage
-------

```python
import asyncio
import time
import random
from siridb.connector import SiriDBClient

async def example(siri):
    # Start connecting to SiriDB.
    # .connect() returns a list of all connections referring to the supplied
    # hostlist. The list can contain exceptions in case a connection could not
    # be made.
    await siri.connect()

    try:
        # insert
        ts = int(time.time())
        value = random.random()
        await siri.insert({'some_measurement': [[ts, value]]})

        # query
        resp = await siri.query('select * from "some_measurement"')
        print(resp)

    finally:
        # Close all SiriDB connections.
        siri.close()


siri = SiriDBClient(
    username='iris',
    password='siri',
    dbname='dbtest',
    hostlist=[('localhost', 9000)],  # Multiple connections are supported
    keepalive=True)

loop = asyncio.get_event_loop()
loop.run_until_complete(example(siri))
```


## SiriDBClient
Create a new SiriDB Client. This creates a new client but `.connect()` must be used to connect.

```python
siri = SiriDBClient(
    username='iris',
    password='siri',
    dbname='dbtest',
    hostlist=[('localhost', 9000)],  # Multiple connections are supported
    keepalive=True)
```
******************************************************************************
Arguments:
* __username__: User with permissions to use the database.
* __password__: Password for the given username.
* __dbname__: Name of the database.
* __hostlist__: List with SiriDB servers. (all servers or a subset of
  servers can be in this list.)

Example:
```python
hostlist=[('server1.local', 9000, {'weight': 3}),
            ('server2.local', 9000),
            ('backup1.local', 9000, {'backup': True})]
```
Each server should at least have a hostname and port
number. Optionally you can provide a dictionary with
extra options.

Available Options:
- weight : Should be a value between 1 and 9. A higher
            value gives the server more weight so it will
            be more likely chosen. (default 1)
- backup : Should be either True or False. When True the
            server will be marked as backup server and
            will only be chosen if no other server is
            available. (default: False)

******************************************************************************

### SiriDBClient.connect

Start connecting to SiriDB. .connect() returns a list of all connections referring to the supplied hostlist. The list can contain exceptions in case a connection could not be made
```
siri.connect()
```

### SiriDBClient.insert

### SiriDBClient.query

### SiriDBClient.close


## Exception codes

## Version info