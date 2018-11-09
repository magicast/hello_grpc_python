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

from __future__ import print_function

import sys
import time

import grpc
from hello_pb2 import HelloRequest, SumRequest
from hello_pb2_grpc import HelloStub


def run(command):
    # create channel
    with grpc.insecure_channel('localhost:10056') as channel:
        # create stub
        hello_stub = HelloStub(channel)

        if command == '1':
            # unary
            response = hello_stub.Say(HelloRequest(message='hello'))
            print('Received: {}'.format(response.message))
        elif command == '2':
            # server streaming
            for response in hello_stub.Notify(HelloRequest(message='hello')):
                print('Received: {}'.format(response.message))
        elif command == '3':
            # client streaming
            def request(count):
                for e in range(count):
                    yield SumRequest(num=e)
                    time.sleep(1)

            print('SUM: {}'.format(hello_stub.Sum(request(10))))
        elif command == '4':
            # bidirectional streaming
            def request(count):
                for e in range(count):
                    yield SumRequest(num=e)
                    time.sleep(1)

            for reply in hello_stub.SumRandom(request(20)):
                print('SUM: {}'.format(reply.sum))


if __name__ == '__main__':
    command_arg = sys.argv[1]
    run(command_arg)
