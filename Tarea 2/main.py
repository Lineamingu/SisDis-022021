import json
from flask import render_template, request, redirect, url_for, Flask
from kafka import KafkaProducer
import sys

# f = open('resumen.json', 'r')
# data = json.load(f)
# f.close()

# f = open('resumen.json', 'w')
# for i in data['tienda']:
#     for j in i:
#         if j == '3':

#             print(i[j]['ganancias_dia'])
#             i[j]['ganancias_dia'] = 100
#             json.dump(data, f, indent=4)
#         # if i[j]['email_vendedor'] == 'javierfeli.urzua@mail.udp.cl':
#         #   print(f'tienda: {j}, cocinero: {i[j]["email_cocinero"]}')

# f.close()

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def main_page():
    if request.method == 'POST':

        nro_tienda = request.form['nro_tienda']
        sopaipillas = request.form['sop']
        completos = request.form['com']
        # request.args.get(key, default=None, type=None)

        f = open('resumen.json', 'r')
        data = json.load(f)
        f.close()

        # f = open('resumen.json', 'w')
        # for i in data['tienda']:
        #     for j in i:
        #         if int(nro_tienda) == int(j):
        #             ganancia_sop = int(sopaipillas) * 150
        #             ganancia_completos = int(completos) * 500
        #             ganancia_total = ganancia_sop + ganancia_completos
        #             i[j]['ventas_sopaipillas'] = i[j]['ventas_sopaipillas'] + \
        #                 int(sopaipillas)
        #             i[j]['ventas_completos'] = i[j]['ventas_completos'] + \
        #                 int(completos)
        #             i[j]['ganancias_dia'] = i[j]['ganancias_dia'] + \
        #                 int(ganancia_total)
        # json.dump(data, f, indent=4)
        # f.close()

        producer = KafkaProducer(value_serializer=lambda m: json.dumps(
            m).encode('ascii'), bootstrap_servers=['localhost:9092'])

        for i in data['tienda']:
            for j in i:
                if int(nro_tienda) == int(j):
                    ganancia_sop = int(sopaipillas) * 150
                    ganancia_completos = int(completos) * 500
                    ganancia_total = ganancia_sop + ganancia_completos
                    ventas_sopaipillas = int(sopaipillas)
                    ventas_completos = int(completos)
                    ganancias_dia = int(ganancia_total)
                    producer.send('topic_orders', {
                        'nro_tienda': int(nro_tienda), 'ventas_sopaipillas': ventas_sopaipillas, 'ventas_completos': ventas_completos, 'ganancias_dia': ganancias_dia})

        producer.flush()

        # esto es en caso de que la redirección venga en el link
        # next = request.args.get('next', None)
        # if next:
        #    return redirect(next)
        return redirect(url_for('main_page'))
    return render_template("index.html")


@ app.route("/daily_summary", methods=["GET", "POST"])
def daily_summary():
    tienda = {}
    tiendas = []
    if request.method == 'POST':

        f = open('resumen.json', 'r')
        data = json.load(f)
        f.close()

        producer = KafkaProducer(value_serializer=lambda m: json.dumps(
            m).encode('ascii'), bootstrap_servers=['localhost:9092'])

        for i in data['tienda']:
            for j in i:
                nro_tienda = j
                email_vendedor = i[j]['email_vendedor']
                email_cocinero = i[j]['email_cocinero']
                ventas_sopaipillas = i[j]['ventas_sopaipillas']
                ventas_completos = i[j]['ventas_completos']
                ganancias_dia = i[j]['ganancias_dia']
                producer.send('daily_summary', {'nro_tienda': int(
                    nro_tienda), 'email_vendedor': email_vendedor, 'email_cocinero': email_cocinero, 'ventas_sopaipillas': int(ventas_sopaipillas), 'ventas_completos': int(ventas_completos), 'ganancias_dia': int(ganancias_dia)})

        producer.flush()
        return redirect(url_for('daily_summary'))
    else:
        f = open('resumen.json', 'r')
        data = json.load(f)
        f.close()

        for i in data['tienda']:
            for j in i:
                tienda = {'nro': j, 'email_vendedor': i[j]['email_vendedor'], 'email_cocinero': i[j]['email_cocinero'], 'sopaipillas': i[j]
                          ['ventas_sopaipillas'], 'completos': i[j]['ventas_completos'], 'ganancias': i[j]['ganancias_dia']}
                tiendas.append(tienda)

        return render_template('daily_summary.html', tiendas=tiendas)


if __name__ == "__main__":
    app.run(debug=True, port=50051)
