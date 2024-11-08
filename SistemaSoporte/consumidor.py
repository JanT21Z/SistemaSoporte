import pika
import mysql.connector

rabbitmq_host = 'localhost'
rabbitmq_queue = 'app_sistemasoporte'
rabbitmq_user = 'root'
rabbitmq_pass = 'admin'

mysql_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'sistemasoporte'
}

def save_to_db(nombre, telefono, requerimiento):
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()
    query = "INSERT INTO REQUERIMIENTO (nombre, telefono, requerimiento) VALUES (%s, %s, %s)"
    cursor.execute(query, (nombre, telefono, requerimiento))
    connection.commit()
    cursor.close()
    connection.close()

def callback(ch, method, properties, body):
    message = body.decode('utf-8')
    nombre, telefono, requerimiento = message.split(',')
    print(f"Mensaje recibido: {nombre}, {telefono}, {requerimiento}")
    save_to_db(nombre, telefono, requerimiento)
    print(f"Guardado en BD: {nombre}, {telefono}, {requerimiento}")


credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
parameters = pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=rabbitmq_queue)
channel.basic_consume(queue=rabbitmq_queue, on_message_callback=callback, auto_ack = True)

print('Esperando Mensajes...')
channel.start_consuming()


