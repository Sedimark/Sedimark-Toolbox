from mage_ai.streaming.sources.base_python import BasePythonSource
from mage_ai.settings.repo import get_repo_path
from websockets.sync.client import connect
from typing import Callable, Any
from threading import Event
from queue import Queue
import asyncio
import yaml
import json

if 'streaming_source' not in globals():
    from mage_ai.data_preparation.decorators import streaming_source


@streaming_source
class CustomSource(BasePythonSource):
    def init_client(self):
        """
        Implement the logic of initializing the client.
        """
        self.stop_event = Event()
        self.update_queue = Queue()
        config_file = get_repo_path() + "/configs/<pipeline_name>/config.yaml"
        self.accuracies = []
        with open(config_file, 'r') as c:
            self.conf = yaml.safe_load(c)

        self.get_node()

        self.generator = self.topology.fit_generator(self.node)
        self.epoch = 0
        self.metric_name = self.conf["model"]["metrics"][0]
        self.websocket_url = "ws:mageapi:8000/mage/ws"

    def send_data(self, data: Any):
        """
        Sends data through the WebSocket connection.
        """
        try:
            with connect(self.websocket_url) as websocket:
                print(f"Seding data to websocket: {data}")
                websocket.send(json.dumps(data), text=True)
        except Exception as e:
            print(f"Error sending data: {e}")

    def get_node(self):
        from shamrock import (
            ConfigLoader,
            ModelLoader,
            TopologyLoader,
            ShamrockDataset,
            ShamrockNode,
        )
        from shamrock.config import Config
        from shamrock.model.builtin import builtin_model

        model_class = builtin_model[self.conf["framework"]][self.conf["model"]["model"]]
        model = model_class()
        self.conf["model"]["model"] = model

        from shamrock.utils.condition import (
            BasicStopCondition,
            FederatedServerStopCondition,
        )

        if self.conf["topology"]["topology_name"] != "FederatedServer":

            condition = BasicStopCondition(stop_event=self.stop_event)
        else:
            condition = FederatedServerStopCondition(stop_event=self.stop_event)
        config_object = Config(**self.conf)
        data = ShamrockDataset(**config_object.dataset)
        model = ModelLoader(**config_object.model)
        topology = TopologyLoader(stop_condition=condition, **config_object.topology)
        node = ShamrockNode(dataset=data, model=model, **config_object.node)
        self.node = node
        self.topology = topology

    def batch_read(self, handler: Callable):
        """
        Batch read the messages from the source and use handler to process the messages.
        """
        while True:
            try:
                for success, metric in self.generator:

                    if success and metric[self.metric_name] is not None:

                        self.update_queue.put(
                            {
                                "type": "loss",
                                "data": {
                                    "loss": metric[self.metric_name],
                                    "epoch": self.epoch,
                                },
                            }
                        )

                        while not self.update_queue.empty():
                            update = self.update_queue.get()
                            if update["type"] == "loss":
                                self.accuracies.append(update["data"]["loss"])
                            elif update["type"] == "error":
                                print(f"Error: {update['data']}", "Training error occurred")
                        
                        handler(self.update_queue)
                                                
                        send_to_ws = {
                            "pipeline": "<pipeline_name>",
                            "type": "json",
                            "data": self.accuracies
                        }

                        self.send_data(send_to_ws)
            except Exception as e:
                import traceback

                print(traceback.format_exc())
                self.update_queue.put({"type": "error", "data": str(e)})
