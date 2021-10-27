import sys
sys.path.append('.')  # why do i have to do this?
from message_broker import AsyncConsumer as Consumer  # make async?
from message_broker import Producer
from pickle import loads, dumps
import asyncio


class JobsQueue:
    def __init__(self):
        self.topic = 'testopic'
        loop = asyncio.get_event_loop()
        self.task = loop.create_task(self._create_consumer())
        self.consumer = None
        self.producer = Producer(value_serializer=dumps)

    async def _create_consumer(self):
        consumer = Consumer(topic=self.topic, value_deserializer=loads)
        await consumer.start()
        return consumer

    async def get(self):
        if not self.consumer:
            self.consumer = await self.task
        return self.consumer.__anext__()

    async def put(self, job):
        self.prepare_for_serialization(job)
        return self.producer.send(self.topic, job)

    @staticmethod
    def prepare_for_serialization(job):
        # to serialize and transmit object to another process (consumer). db_conn will be assigned after deserialization
        job.db_conn = None

    def empty(self):
        return False  # https://stackoverflow.com/questions/36428014/check-if-kafka-queue-is-empty
