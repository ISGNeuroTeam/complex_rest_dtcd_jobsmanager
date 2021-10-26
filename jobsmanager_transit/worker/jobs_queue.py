import sys
sys.path.append('.')  # why do i have to do this?
from message_broker import AsyncConsumer as Consumer  # make async?
from message_broker import Producer
from pickle import loads, dumps
import asyncio


class JobsQueue:
    def __init__(self):
        self.topic = 'testopic'
        loop = asyncio.get_running_loop()
        # self.task = None
        self.task = loop.create_task(self._create_consumer())
        self.consumer = None
        # self.consumer = Consumer(topic=self.topic, value_deserializer=loads)  # error
        self.producer = Producer(value_serializer=dumps)

    async def _create_consumer(self):
        return Consumer(topic=self.topic, value_deserializer=loads)

    async def get(self):
        if not self.consumer:
            self.consumer = await self.task
        print('in get')
        return self.consumer.__anext__()

    async def put(self, job):
        return self.producer.send(self.topic, job)

    def empty(self):
        return False  # https://stackoverflow.com/questions/36428014/check-if-kafka-queue-is-empty
