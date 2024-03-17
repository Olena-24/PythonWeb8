import pika
import sys
import os
from user_model import User

def main():
   
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

   
    queue_name = 'hw_8'
    channel.queue_declare(queue=queue_name, durable=True)

   
    def callback(ch, method, properties, body):
       
        pk = body.decode()
       
        user = User.objects(id=pk, completed=False).first()
       
        if user:
            user.update(set__completed=True)
       
        ch.basic_ack(delivery_tag=method.delivery_tag)

 
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

