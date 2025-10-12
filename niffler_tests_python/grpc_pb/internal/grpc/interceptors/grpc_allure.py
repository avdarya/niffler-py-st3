from typing import Callable

import allure
import grpc
from google.protobuf.message import Message
from google.protobuf.json_format import MessageToJson

class GRPCAllureInterceptor(grpc.UnaryUnaryClientInterceptor):

    def intercept_unary_unary(
            self,
            continuation: Callable,
            client_call_details: grpc.ClientCallDetails,
            request: Message
    ) -> Callable:
        with allure.step(client_call_details.method):
            allure.attach(
                MessageToJson(request),
                "request",
                attachment_type=allure.attachment_type.JSON
            )
            response = continuation(client_call_details, request)
            try:
                allure.attach(
                    MessageToJson(response.result()),
                    "response",
                    attachment_type=allure.attachment_type.JSON
                )
            except grpc.RpcError as e:
                allure.attach(
                    f"gRPC error: {e.code().name} - {e.details()}",
                    "error",
                    attachment_type=allure.attachment_type.TEXT
                )
            return response

