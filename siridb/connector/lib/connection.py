
class SiriDBConnection():

    def __init__(self,
                username,
                password,
                dbname,
                host='127.0.0.1',
                port=c.DEFAULT_CLIENT_PORT,
                loop=None,
                timeout=10,
                protocol=SiriClientProtocol):
        self._loop = loop or asyncio.get_event_loop()
        client = self._loop.create_connection(
            lambda: protocol(username, password, dbname),
            host=host,
            port=port)
        self._transport, self._protocol = self._loop.run_until_complete(
            asyncio.wait_for(client, timeout=timeout))
        self._loop.run_until_complete(self._protocol.auth_future)

    def close(self):
        if hasattr(self, '_protocol') and hasattr(self._protocol, 'transport'):
            self._protocol.transport.close()

    def query(self, query, time_precision=None, timeout=30):
        result = self._loop.run_until_complete(
            self._protocol.send_package(npt.CPROTO_REQ_QUERY,
                                        data=(query, time_precision),
                                        timeout=timeout))
        return result

    def insert(self, data, timeout=600):
        result = self._loop.run_until_complete(
            self._protocol.send_package(npt.CPROTO_REQ_INSERT,
                                        data=data,
                                        timeout=timeout))
        return result

    def _register_server(self, server, timeout=30):
        '''Register a new SiriDB Server.

        This method is used by the SiriDB manage tool and should not be used
        otherwise. Full access rights are required for this request.
        '''
        result = self._loop.run_until_complete(
            self._protocol.send_package(npt.CPROTO_REQ_REGISTER_SERVER,
                                        data=server,
                                        timeout=timeout))
        return result

    def _get_file(self, fn, timeout=30):
        '''Request a SiriDB configuration file.

        This method is used by the SiriDB manage tool and should not be used
        otherwise. Full access rights are required for this request.
        '''
        msg = npt.FILE_MAP.get(fn, None)
        if msg is None:
            raise FileNotFoundError('Cannot get file {!r}. Available file '
                                    'requests are: {}'
                                    .format(fn, ', '.join(npt.FILE_MAP.keys())))
        result = self._loop.run_until_complete(
            self._protocol.send_package(msg, timeout=timeout))
        return result


class SiriDBAsyncConnection():

    _protocol = None
    _keepalive = None

    async def keepalive_loop(self, interval=45):
        sleep = interval
        while True:
            await asyncio.sleep(sleep)
            if not self.connected:
                break
            sleep = \
                max(0, interval - time.time() + self._last_resp) or interval
            if sleep == interval:
                logging.debug('Send keep-alive package...')
                try:
                    await self._protocol.send_package(npt.CPROTO_REQ_PING,
                                                      timeout=15)
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logging.error(e)
                    self.close()
                    break

    async def connect(self,
                      username,
                      password,
                      dbname,
                      host='127.0.0.1',
                      port=c.DEFAULT_CLIENT_PORT,
                      loop=None,
                      timeout=10,
                      keepalive=False,
                      protocol=SiriClientProtocol):
        loop = loop or asyncio.get_event_loop()
        client = loop.create_connection(
            lambda: protocol(username, password, dbname),
            host=host,
            port=port)
        self._timeout = timeout
        _transport, self._protocol = \
            await asyncio.wait_for(client, timeout=timeout)
        await self._protocol.auth_future
        self._last_resp = time.time()
        if keepalive and (self._keepalive is None or self._keepalive.done()):
            self._keepalive = asyncio.ensure_future(self.keepalive_loop())

    def close(self):
        if self._keepalive is not None:
            self._keepalive.cancel()
            del self._keepalive
        if self._protocol is not None:
            self._protocol.transport.close()
            del self._protocol

    async def query(self, query, time_precision=None, timeout=3600):
        result = await self._protocol.send_package(
            npt.CPROTO_REQ_QUERY,
            data=(query, time_precision),
            timeout=timeout)
        self._last_resp = time.time()
        return result

    async def insert(self, data, timeout=3600):
        result = await self._protocol.send_package(
            npt.CPROTO_REQ_INSERT,
            data=data,
            timeout=timeout)
        self._last_resp = time.time()
        return result

    @property
    def connected(self):
        return self._protocol is not None and self._protocol._connected