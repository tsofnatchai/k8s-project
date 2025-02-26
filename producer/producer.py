import pika, logging, sys, argparse
from argparse import RawTextHelpFormatter
from time import sleep
import os

if __name__ == '__main__':
    examples = sys.argv[0] + " -p 5672 -s rabbitmq -m 'Hello' "
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter,
                                 description='Run producer.py',
                                 epilog=examples)
    parser.add_argument('-p', '--port', action='store', dest='port', default='5672', help='The port to listen on.')
    parser.add_argument('-s', '--server', action='store', dest='server', default='rabbitmq', help='The RabbitMQ server.')

    parser.add_argument('-m', '--message', action='store', dest='message', help='The message to send', required=False, default='Hello')
    parser.add_argument('-r', '--repeat', action='store', dest='repeat', help='Number of times to repeat the message', required=False, default='30')

    args = parser.parse_args()
    if args.port == None:
        print("Missing required argument: -p/--port")
        sys.exit(1)
    if args.server == None:
        print("Missing required argument: -s/--server")
        sys.exit(1)

    # sleep a few seconds to allow RabbitMQ server to come up
    sleep(10)

    logging.basicConfig(level=logging.INFO)
    LOG = logging.getLogger(__name__)
    rabbitmq_user = os.getenv('RABBITMQ_USER', 'guest')  # Default to 'guest' if not set
    rabbitmq_password = os.getenv('RABBITMQ_PASSWORD', 'guest')  # Default to 'guest' if not set

    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    parameters = pika.ConnectionParameters(args.server,
                                           int(args.port),
                                           '/',
                                           credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    q = channel.queue_declare(queue='pc', durable=True)
    q_name = q.method.queue

    # Turn on delivery confirmations
    channel.confirm_delivery()

    while True:
        if channel.basic_publish('', q_name, args.message):
            LOG.info('Message has been delivered')
        else:
            LOG.warning('Message NOT delivered')

        sleep(2)

    connection.close()