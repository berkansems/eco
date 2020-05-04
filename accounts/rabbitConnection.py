import pika
import logging

logger=logging.getLogger("logger2")

class RabbitConnection():
    channel = pika.adapters.blocking_connection.BlockingChannel
    def __init__(self):
        server_down = True
        while server_down:
            try:
                self.initialize_connection(host='localhost')
                server_down = False
                logger.info('server is up!')

            except:
                server_down = True
                logger.warning('Cannot connect to rabbitmq server.')


    def initialize_connection(self,host):
        logger.info('Attempting to establish RabbitMQ connection')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        # Create a new channel with the next available channel number or pass in a channel number to use
        logger.info('connected')


    def write_to_queue(self,message,route):

        channel = self.connection.channel()


        # Declare queue, create if needed. This method creates or checks a queue. When creating a new queue the client can specify various properties that control the durability of the queue and its contents, and the level of sharing for the queue.
        channel.queue_declare(queue='authorized', durable=True)
        channel.queue_declare(queue='notauthorized', durable=True)
        if(route==1):
            channel.basic_publish(exchange='authentication', routing_key='permited', body=message)
        if(route==2):
            channel.basic_publish(exchange='authentication', routing_key='notpermited', body=message)