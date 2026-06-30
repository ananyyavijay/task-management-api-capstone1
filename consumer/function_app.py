import azure.functions as func
import logging

app = func.FunctionApp()

@app.service_bus_queue_trigger(
    arg_name="msg",
    queue_name="task-api-notifications",
    connection="SERVICE_BUS_CONNECTION"
)
def service_bus_consumer(msg: func.ServiceBusMessage):
    body = msg.get_body().decode("utf-8")

    logging.info("Received message")
    logging.info(body)