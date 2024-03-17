from faker import Faker
from models import Contact
from connect import connect, channel, connection

# Параметры RabbitMQ
channel.queue_declare(queue='contacts')
channel.queue_declare(queue='sms_contacts')
channel.queue_declare(queue='email_contacts')

# Генерация фейковых контактов и сохранение в базу данных
def create_fake_contacts(num_contacts):
    fake = Faker('uk_UA')
    for count in range(num_contacts):
        fullname = fake.name()
        email = fake.email()
        phone_number = fake.phone_number()
        contact = Contact(fullname=fullname, email=email, phone_number=phone_number)
        # Сохраняем контакт
        contact.save()

        if count % 2 == 0:
            # Отправка email
            channel.basic_publish(exchange='', routing_key='email_contacts', body=str(contact.id))
        else:
            # Отправка sms
            channel.basic_publish(exchange='', routing_key='sms_contacts', body=str(contact.id))
        print(f"Добавлен контакт: {fullname}, {email}, {phone_number}")

if __name__ == "__main__":
    num_contacts = 100
    create_fake_contacts(num_contacts)
    connection.close()