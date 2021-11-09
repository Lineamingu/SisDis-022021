from kafka import KafkaConsumer
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


consumer = KafkaConsumer('daily_summary',
                         bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda m: json.loads(m.decode('ascii')))

mensaje = {}
mensajes = []
recipients = []

for message in consumer:
    # print("%s:%d:%d: key=%s value=%s" % (message.topic,
    #                                      message.partition, message.offset, message.key, message.value))

    nro_tienda = message.value['nro_tienda']
    email_vendedor = message.value['email_vendedor']
    email_cocinero = message.value['email_cocinero']
    ventas_sopaipillas = message.value['ventas_sopaipillas']
    ventas_completos = message.value['ventas_completos']
    ganancias_dia = message.value['ganancias_dia']
    mensaje = {nro_tienda: {'email_vendedor': email_vendedor, 'email_cocinero': email_cocinero,
                            'ventas_sopaipillas': ventas_sopaipillas, 'ventas_completos': ventas_completos, 'ganancias_dia': ganancias_dia}}
    recipients.append(email_vendedor)
    recipients.append(email_cocinero)
    # print(f'\n{mensaje}')
    mensajes.append(mensaje)

    f = open('resumen.json', 'r')
    data = json.load(f)
    f.close()

    f = open('resumen.json', 'w')
    for i in data['tienda']:
        for j in i:
            i[j]['ventas_sopaipillas'] = 0
            i[j]['ventas_completos'] = 0
            i[j]['ganancias_dia'] = 0
    json.dump(data, f, indent=4)
    f.close()

    if nro_tienda == 4:
        body = json.dumps(mensajes, indent=4)
        print(f'\n{body}')
        print("Información obtenida.")
        # create message object instance
        msg = MIMEMultipart()

        # setup the parameters of the message
        password = "amogus123"
        msg['From'] = "tareasisdis1@gmail.com"
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = "Resumen de ventas carritos"

        # add in the message body
        msg.attach(MIMEText(body, 'plain'))

        # create server
        server = smtplib.SMTP('smtp.gmail.com: 587')

        server.starttls()

        # Login Credentials for sending the mail
        server.login(msg['From'], password)

        # send the message via the server.
        server.sendmail(msg['From'], recipients, msg.as_string())

        server.quit()

        print("Mails enviados exitosamente.")
        mensaje = {}
        mensajes = []
        recipients = []
