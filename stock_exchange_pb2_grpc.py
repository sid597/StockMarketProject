# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import stock_exchange_pb2 as protos_dot_stock__exchange__pb2


class StockExchangeStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.OrderCreate = channel.unary_unary(
        '/StockExchange/OrderCreate',
        request_serializer=protos_dot_stock__exchange__pb2.OrderCreateRequest.SerializeToString,
        response_deserializer=protos_dot_stock__exchange__pb2.OrderStatusResponse.FromString,
        )
    self.OrderStatus = channel.unary_unary(
        '/StockExchange/OrderStatus',
        request_serializer=protos_dot_stock__exchange__pb2.OrderIdRequest.SerializeToString,
        response_deserializer=protos_dot_stock__exchange__pb2.OrderStatusResponse.FromString,
        )
    self.OrderCancel = channel.unary_unary(
        '/StockExchange/OrderCancel',
        request_serializer=protos_dot_stock__exchange__pb2.OrderIdRequest.SerializeToString,
        response_deserializer=protos_dot_stock__exchange__pb2.OrderStatusResponse.FromString,
        )
    self.UserOrders = channel.unary_unary(
        '/StockExchange/UserOrders',
        request_serializer=protos_dot_stock__exchange__pb2.UserRequest.SerializeToString,
        response_deserializer=protos_dot_stock__exchange__pb2.MultiOrderStatusResponse.FromString,
        )
    self.StockVolume1h = channel.unary_unary(
        '/StockExchange/StockVolume1h',
        request_serializer=protos_dot_stock__exchange__pb2.StockRequest.SerializeToString,
        response_deserializer=protos_dot_stock__exchange__pb2.VolumeResponse.FromString,
        )
    self.StockPrice1h = channel.unary_unary(
        '/StockExchange/StockPrice1h',
        request_serializer=protos_dot_stock__exchange__pb2.StockRequest.SerializeToString,
        response_deserializer=protos_dot_stock__exchange__pb2.PriceResponse.FromString,
        )
    self.OHLC = channel.unary_unary(
        '/StockExchange/OHLC',
        request_serializer=protos_dot_stock__exchange__pb2.OHLCRequest.SerializeToString,
        response_deserializer=protos_dot_stock__exchange__pb2.OHLCResponse.FromString,
        )


class StockExchangeServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def OrderCreate(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def OrderStatus(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def OrderCancel(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def UserOrders(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def StockVolume1h(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def StockPrice1h(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def OHLC(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_StockExchangeServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'OrderCreate': grpc.unary_unary_rpc_method_handler(
          servicer.OrderCreate,
          request_deserializer=protos_dot_stock__exchange__pb2.OrderCreateRequest.FromString,
          response_serializer=protos_dot_stock__exchange__pb2.OrderStatusResponse.SerializeToString,
      ),
      'OrderStatus': grpc.unary_unary_rpc_method_handler(
          servicer.OrderStatus,
          request_deserializer=protos_dot_stock__exchange__pb2.OrderIdRequest.FromString,
          response_serializer=protos_dot_stock__exchange__pb2.OrderStatusResponse.SerializeToString,
      ),
      'OrderCancel': grpc.unary_unary_rpc_method_handler(
          servicer.OrderCancel,
          request_deserializer=protos_dot_stock__exchange__pb2.OrderIdRequest.FromString,
          response_serializer=protos_dot_stock__exchange__pb2.OrderStatusResponse.SerializeToString,
      ),
      'UserOrders': grpc.unary_unary_rpc_method_handler(
          servicer.UserOrders,
          request_deserializer=protos_dot_stock__exchange__pb2.UserRequest.FromString,
          response_serializer=protos_dot_stock__exchange__pb2.MultiOrderStatusResponse.SerializeToString,
      ),
      'StockVolume1h': grpc.unary_unary_rpc_method_handler(
          servicer.StockVolume1h,
          request_deserializer=protos_dot_stock__exchange__pb2.StockRequest.FromString,
          response_serializer=protos_dot_stock__exchange__pb2.VolumeResponse.SerializeToString,
      ),
      'StockPrice1h': grpc.unary_unary_rpc_method_handler(
          servicer.StockPrice1h,
          request_deserializer=protos_dot_stock__exchange__pb2.StockRequest.FromString,
          response_serializer=protos_dot_stock__exchange__pb2.PriceResponse.SerializeToString,
      ),
      'OHLC': grpc.unary_unary_rpc_method_handler(
          servicer.OHLC,
          request_deserializer=protos_dot_stock__exchange__pb2.OHLCRequest.FromString,
          response_serializer=protos_dot_stock__exchange__pb2.OHLCResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'StockExchange', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
