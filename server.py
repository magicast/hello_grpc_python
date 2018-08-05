# coding=utf-8

"""
Copyright 2018 magicast.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from concurrent import futures
import time

import random

import grpc
from hello_pb2 import HelloReply, SumReply
from hello_pb2_grpc import HelloServicer, add_HelloServicer_to_server


class Hello(HelloServicer):
    # unary
    def Say(self, request, context):
        print('REQUEST:', request.message)
        response_message = 'You said: {}!'.format(request.message)
        print('RESPONSE:', response_message)
        return HelloReply(message=response_message)

    # server streaming
    def Notify(self, request, context):
        for e in range(10):
            time.sleep(1)
            response_message = 'you said: {}: {}'.format(request.message, e)
            yield HelloReply(message=response_message)
        print('END')

    # client streaming
    def Sum(self, request_iterator, context):
        requests = []
        for request in request_iterator:
            requests.append(request.num)
        result = sum(requests)
        print('SUM={}: {}'.format(result, requests))
        return SumReply(sum=result)

    # bidirectional streaming
    def SumRandom(self, request_iterator, context):
        requests = []
        for request in request_iterator:
            requests.append(request.num)
            if random.random() > 0.6:
                result = sum(requests)
                print('SUM={}: {}'.format(result, requests))
                requests = []
                yield SumReply(sum=result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    add_HelloServicer_to_server(Hello(), server)

    server.add_insecure_port('[::]:30011')
    server.start()
    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
