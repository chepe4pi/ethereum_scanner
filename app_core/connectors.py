from constance import config
from web3 import RPCProvider, Web3


class RpcServerConnector:
    def __init__(self, rpc_provider_host=config.RPC_SERVER_HOST, rpc_provider_port=config.RPC_SERVER_PORT):
        """
        :type rpc_provider_host: str
        :type rpc_provider_port: str
        :rtype: web3.Web3
        """
        self.rpc_provider_host = rpc_provider_host
        self.rpc_provider_port = rpc_provider_port

    def __call__(self, *args, **kwargs):
        return self.get_connection()

    def get_connection(self):
        return Web3(RPCProvider(host=self.rpc_provider_host, port=self.rpc_provider_port))
