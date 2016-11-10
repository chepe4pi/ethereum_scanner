from constance import config
from web3 import RPCProvider, Web3, IPCProvider


class RpcServerConnector:
    def __call__(self, *args, **kwargs):
        return self.get_connection()

    def get_connection(self):
        if config.RPC_SERVER_PROTOCOL == 'IPC':
            return Web3(IPCProvider(ipc_path=config.RPC_SERVER_IPC_PATH))
        elif config.RPC_SERVER_PROTOCOL == 'HTTP':
            return Web3(RPCProvider(host=config.RPC_SERVER_HOST, port=config.RPC_SERVER_PORT))
        else:
            raise ValueError('wrong or missing RPC_SERVER_PROTOCOL')
