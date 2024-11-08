import pika
from flask import Flask, request, jsonify

app = Flask(__name__)

rabbitmq_host = 'localhost'
rabbitmq_queue = 'app_sistemasoporte'
rabbitmq_user = 'root'
rabbitmq_pass = 'admin'

def send_to_queue(message):
    try:
        print("Conectando a RabbitMQ...")
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=rabbitmq_host,
            credentials=pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
        ))
        channel = connection.channel()
        
        channel.queue_declare(queue=rabbitmq_queue, durable=False)
        
        channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=message)
        
        print("Mensaje enviado a la cola de RabbitMQ:", message)
        connection.close()
        
    except Exception as e:
        print(f"Error al enviar a RabbitMQ: {e}")


@app.route('/api/soporte', methods=['POST'])
def soporte():
    data = request.get_json()
    nombre = data.get('nombre')
    telefono = data.get('telefono')
    requerimiento = data.get('requerimiento')

    message = f"{nombre},{telefono},{requerimiento}"
    send_to_queue(message)

    return jsonify({"message": "Solicitud de soporte recibida"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


