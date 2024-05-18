import pika
from models import Contact
import connect


RABBITMQ_QUEUE = "email_campaign"

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue = RABBITMQ_QUEUE)

def send_email(contact):
    print(f"Sending email to {contact.full_name} at {contact.email}")

    contact.email_sent = True
    contact.save()

def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects(id = contact_id).first()
    if contact:
        send_email(contact)
        print(f"Email sent to {contact.email} and status updated.")


channel.basic_consume(queue = RABBITMQ_QUEUE, on_message_callback = callback, auto_ack=True)
print(f'Waiting for messages in {RABBITMQ_QUEUE} queue. To exit press CTRL+C')

channel.start_consuming()
