from typing import Callable

import grpc
from google.protobuf.message import Message

class GRPCLoggingInterceptor(grpc.UnaryUnaryClientInterceptor):

    def intercept_unary_unary(
            self,
            continuation: Callable,
            client_call_details: grpc.ClientCallDetails,
            request: Message
    ) -> Callable:
        response = continuation(client_call_details, request)
        return response

