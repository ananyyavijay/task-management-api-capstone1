import json
import logging
import os

from azure.servicebus import ServiceBusClient, ServiceBusMessage

logger = logging.getLogger(__name__)

SERVICE_BUS_CONNECTION = os.getenv("SERVICE_BUS_CONNECTION")
QUEUE_NAME = os.getenv("SERVICE_BUS_QUEUE_NAME")


def publish_task_assignment(message: dict):
    """
    Publish assignment notification to Azure Service Bus.
    Raises exceptions so caller can decide whether to ignore/log.
    """

    client = ServiceBusClient.from_connection_string(
        SERVICE_BUS_CONNECTION
    )

    with client:
        sender = client.get_queue_sender(queue_name=QUEUE_NAME)

        with sender:
            sender.send_messages(
                ServiceBusMessage(json.dumps(message))
            )