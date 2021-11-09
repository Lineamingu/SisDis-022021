from kafka import KafkaConsumer
import json
consumer = KafkaConsumer('topic_orders',
                         bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda m: json.loads(m.decode('ascii')))

for message in consumer:
    print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                         message.offset, message.key,
                                         message.value))

    nro_tienda = int(message.value['nro_tienda'])
    ventas_sopaipillas = int(message.value['ventas_sopaipillas'])
    ventas_completos = int(message.value['ventas_completos'])
    ganancias_dia = int(message.value['ganancias_dia'])

    f = open('resumen.json', 'r')
    data = json.load(f)
    f.close()

    f = open('resumen.json', 'w')
    for i in data['tienda']:
        for j in i:
            if nro_tienda == int(j):
                i[j]['ventas_sopaipillas'] = i[j]['ventas_sopaipillas'] + \
                    ventas_sopaipillas
                i[j]['ventas_completos'] = i[j]['ventas_completos'] + ventas_completos
                i[j]['ganancias_dia'] = i[j]['ganancias_dia'] + ganancias_dia
    json.dump(data, f, indent=4)
    f.close()
    print("Inventario actualizado")
