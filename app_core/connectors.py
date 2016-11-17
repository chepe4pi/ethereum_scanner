import json
from json import JSONDecodeError

from constance import config
import gevent
from gevent import socket
from web3 import RPCProvider, Web3
from web3.providers.base import BaseProvider
from web3.providers.ipc import get_default_ipc_path, get_ipc_socket
from web3.utils.string import force_text


class AsyncIPCProvider(BaseProvider):
    def __init__(self, ipc_path=None, testnet=False, *args, **kwargs):
        if ipc_path is None:
            self.ipc_path = get_default_ipc_path(testnet)
        else:
            self.ipc_path = ipc_path

        super(AsyncIPCProvider, self).__init__(*args, **kwargs)

    def make_request(self, method, params):
        request = self.encode_rpc_request(method, params)

        with get_ipc_socket(self.ipc_path) as sock:
            sock.sendall(request)
            response_raw = b""

            with gevent.Timeout(10):
                while True:
                    try:
                        response_raw += sock.recv(4096)
                    except socket.timeout:
                        gevent.sleep(0)
                        continue

                    if response_raw == b"":
                        gevent.sleep(0)
                    else:
                        try:
                            json.loads(force_text(response_raw))
                        except JSONDecodeError:
                            gevent.sleep(0)
                            continue
                        else:
                            break

        return response_raw


class RpcServerConnector:
    def __call__(self, *args, **kwargs):
        return self.get_connection()

    def get_connection(self):
        if config.RPC_SERVER_PROTOCOL == 'IPC':
            return Web3(AsyncIPCProvider(ipc_path=config.RPC_SERVER_IPC_PATH))
        elif config.RPC_SERVER_PROTOCOL == 'HTTP':
            return Web3(RPCProvider(host=config.RPC_SERVER_HOST, port=config.RPC_SERVER_HTTP_PORT))
        else:
            raise ValueError('wrong or missing RPC_SERVER_PROTOCOL')
