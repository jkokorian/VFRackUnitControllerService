import zmq

from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.zmq import ZmqClientTransport
from tinyrpc import RPCClient

ctx = zmq.Context()

rpc_client = RPCClient(
    JSONRPCProtocol(),
    ZmqClientTransport.create(ctx, 'tcp://127.0.0.1:5050')
)


remote_server = rpc_client.get_proxy()

print remote_server.gotoStopState()