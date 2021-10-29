from message_broker import Producer
# from cloudpickle import dumps, register_pickle_by_value
from json import dumps
import asyncio
import logging
from jobsmanager_transit.ot_simple_rest.utils.primitives import EverythingEqual
# from jobsmanager_transit.ot_simple_rest.jobs_manager import jobs
# from message_broker import AsyncConsumer as Consumer  # make async?

log = logging.getLogger('jobsmanager_transit')
log.info('plugin works at jobs_queue')


class JobsQueue:
    def __init__(self):
        self.topic = 'testopic'
        loop = asyncio.get_event_loop()
        # self.task = loop.create_task(self._create_consumer())
        # self.consumer = None
        # register_pickle_by_value(jobs)
        self.producer = Producer(value_serializer=lambda x: dumps(x).encode('utf-8'))

    # async def _create_consumer(self):
    #     consumer = Consumer(topic=self.topic, value_deserializer=loads)
    #     await consumer.start()
    #     return consumer

    # async def get(self):
    #     if not self.consumer:
    #         self.consumer = await self.task
    #     return await self.consumer.__anext__()

    async def put(self, job):
        log.info('<prepare for serialization')
        serializable = self._prepare_for_serialization(job)
        log.info('<send message')
        self.producer.send(self.topic, serializable)  # ?

    @staticmethod
    def _convert_to_str(request_data):
        for data in request_data.values():
            data[0] = data[0].decode('utf-8')

    def _prepare_for_serialization(self, job):
        # to serialize and transmit object to another process (consumer). db will be assigned after deserialization
        job.db = None
        job.logger = None
        self._convert_to_str(job.request.arguments)
        if isinstance(job.indexes[0], EverythingEqual):
            job.indexes = ['*']  # * means that EverythingEqual object is used
        else:
            pass  # todo authorization
        job.request = job.request.__dict__
        return job.__dict__  # some useless fields are passed

    # def empty(self):
    #     return False  # https://stackoverflow.com/questions/36428014/check-if-kafka-queue-is-empty
