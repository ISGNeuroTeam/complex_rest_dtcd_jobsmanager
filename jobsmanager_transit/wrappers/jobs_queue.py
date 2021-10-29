from message_broker import Producer
from json import dumps
from datetime import datetime
import logging

log = logging.getLogger('jobsmanager_transit')


class JobsQueue:
    def __init__(self):
        self.topic = 'testopic'
        self.producer = Producer(value_serializer=lambda x: dumps(x).encode('utf-8'))

    async def put(self, job_description):
        log.info('<send message')
        # self._convert_to_str(job_description['body_arguments'])
        topic, partition, offset = self.producer.send(self.topic, job_description)
        return {"status": "success", "timestamp": str(datetime.now()), 'topic': topic, 'partition': partition, 'offset': offset}

    @staticmethod
    def _convert_to_str(request_data):
        for data in request_data.values():
            data[0] = data[0].decode('utf-8')
