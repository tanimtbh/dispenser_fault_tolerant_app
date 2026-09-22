from framework.core import Worker
import asyncio
import logging
import time

logger = logging.getLogger(__name__)

class DespenseUnitWorker(Worker):
    def __init__(self, name, client, slave_id=None):
        super().__init__(name)
        self.client = client
        self.slave_id = slave_id

    async def handle(self, msg):
        future = None
        if isinstance(msg, tuple):
            msg, future = msg
            print("Tuple msg received:", msg)
            print("Tuple future received:", future)
           
        required_fields = {"req_id", "id", "weight"}
        if not required_fields.issubset(msg.keys()):
            response = {"action":"dispense", "data": {"status": "error", "message": "Missing required fields."}}
            logger.warning(f"[{self.name}] {response['data']['message']}")
            if future:
                future.set_result(response)
            return response
        
        if msg["req_id"] == "crash":
            #raise RuntimeError(f"[{self.name}] intentional crash triggered!")
            21 / 0 # trigger ZeroDivisionError

        print("Received msg:", msg)
        # proper response initialize
        return response


class ElevatorWorker(Worker):
    def __init__(self, name, client, slave_id=None):
        super().__init__(name)
        self.client = client
        self.slave_1_id = slave_id
        self.slave_2_id = slave_id + 1

class StatusTask:
    def __init__(self, worker, publish_func=None):
        self.worker = worker
        self.name = f"{worker.name}_status_task"
        self.publish_func = publish_func  
    async def run(self):
        while True:
            await asyncio.sleep(20)  # Publish every 1 second