import pika
from faker import Faker
from models import Contact
import connect


RABBITMQ_QUEUE = "email_campaign"

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port = 5672, credentials = credentials))
channel = connection.channel()
channel.queue_declare(queue = RABBITMQ_QUEUE)

fake = Faker()
num_contacts = 10 

for _ in range(num_contacts):
    contact = Contact(
        full_name = fake.name(),
        email = fake.email()
    )
    contact.save()

    channel.basic_publish(exchange = '', routing_key = RABBITMQ_QUEUE, body = str(contact.id))

print(f'Sent {num_contacts} messages to {RABBITMQ_QUEUE} queue.')

connection.close()
