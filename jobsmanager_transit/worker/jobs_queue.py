import sys
sys.path.append('.')  # why do i have to do this?
from message_broker import AsyncConsumer as Consumer  # make async?
from message_broker import Producer
from pickle import loads, dumps
import asyncio


class JobsQueue:
    def __init__(self):
        self.topic = 'testopic'
        self.consumer = Consumer(topic=self.topic, value_deserializer=loads)  # error
        self.producer = Producer(value_serializer=dumps)

    async def get(self):
        return self.consumer.__anext__().value

    async def put(self, job):
        return self.producer.send(self.topic, job)

    def empty(self):
        return False  # https://stackoverflow.com/questions/36428014/check-if-kafka-queue-is-empty
