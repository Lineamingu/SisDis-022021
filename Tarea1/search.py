import search_pb2 as pb2
import search_pb2_grpc as pb2_grpc
import grpc
import redis
import json
from searchform import ProductSearchForm
from flask import Flask, jsonify, flash, render_template, request, redirect
import sys
app = Flask(__name__)


class SearchClient(object):
    """
    Client for gRPC functionality
    """

    def __init__(self):
        self.host = 'localhost'
        self.server_port = 50051

        # instantiate a channel
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port))

        # bind the client and the server
        self.stub = pb2_grpc.SearchStub(self.channel)

    def get_url(self, message):
        """
        Client function to call the rpc for GetServerResponse
        """
        message = pb2.Message(message=message)
        print(f'{message}')
        return self.stub.GetServerResponse(message)


r = redis.Redis(host='localhost', port=6379, db=0)


@app.route('/', methods=['GET', 'POST'])
def index():
    search = ProductSearchForm(request.form)
    if request.method == 'POST':
        return getProduct(search)
    return render_template('index.html', form=search)


@app.route('/results')
def getProduct(search):

    r = redis.Redis(host='localhost', port=6379, db=0)

    search_string = search.data['search']
    # print(search_string)
    search_results = search_string.lower()
    results = []

    value = r.get(f'results: {search_results}')
    if value:
        print(f'La búsqueda de {search_results} se encontró en cache.')
        result = value.decode()
        results = result.replace("[", "")
        result = results.replace("]", "")
        results = result.split("'{")
        final = []
        for i in results:
            result = i.replace("}',", "")
            final.append(result)
        return jsonify({'resultados': final})
        #result = jsonify({'resultados': result})
        # return result
    else:
        print(f'La búsqueda de {search_results} no se encontró en cache.')
        client = SearchClient()
        result = client.get_url(search_results)
        # print(len(result.product))
        if (len(result.product) > 0):
            for i in result.product:
                res = "{" + f'id: "{str(i.id).strip()}",' + f'brand_name: "{str(i.brand_name).strip()}",' + f'items_description: "{str(i.items_description).strip()}",' + \
                    f'prices: "{str(i.prices).strip()}",' + \
                    f'category: "{str(i.category).strip()}"' + "}"
                results.append(res)
            r.set(f'results: {search_results}', str(results))
            return jsonify({'resultados': results})

        return "No se encontraron resultados."


if __name__ == "__main__":
    app.run(debug=True, port=50051)
