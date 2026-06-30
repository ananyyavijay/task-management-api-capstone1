import json
import logging

import azure.functions as func

app = func.FunctionApp()


@app.service_bus_queue_trigger(
    arg_name="msg",
    queue_name="task-api-notifications",
    connection="SERVICE_BUS_CONNECTION",
)
def service_bus_consumer(msg: func.ServiceBusMessage):

    body = msg.get_body().decode("utf-8")

    logging.info("=" * 60)
    logging.info("SERVICE BUS MESSAGE RECEIVED")
    logging.info("=" * 60)

    logging.info(body)

    try:
        data = json.loads(body)

        logging.info(f"Task ID      : {data.get('task_id')}")
        logging.info(f"Assigned To  : {data.get('assigned_to')}")
        logging.info(f"Assigned By  : {data.get('assigned_by')}")
        logging.info(f"Priority     : {data.get('priority')}")
        logging.info(f"Status       : {data.get('status')}")

    except Exception as e:
        logging.error(e)