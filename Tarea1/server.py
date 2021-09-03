import grpc
from concurrent import futures
import search_pb2_grpc as pb2_grpc
import search_pb2 as pb2
import json


class SearchService(pb2_grpc.SearchServicer):

    def __init__(self, *args, **kwargs):
        pass

    def GetServerResponse(self, request, context):
        count = 0
        results = []
        message_og = request.message
        message = message_og.lower()
        # result = {'id': 80, 'brand_name': "AMD", 'items_description':
        #           "CORSAIR Vengeance RGB Pro 16GB (2 x 8GB) 288-Pin DDR4 SDRAM DDR4 3600 (PC4 28...", 'prices': 14723.99, 'category': "cpu"}

        # results = [result]

        # result2 = {'id': 70, 'brand_name': "AMD", 'items_description':
        #            "CORSAIR Vengeance", 'prices': 14000.99, 'category': "cpu"}

        # results.append(result2)

        f = open('inventory.json',)

        data = json.load(f)

        for i in data:
            # print(i["items_description"])
            if str(message) in i["items_description"].lower() or message in str(i["id"]).lower() or message in i["brand_name"].lower() or message in str(i["prices"]).lower() or message in i["category"].lower():
                #print(f'"{str(i["id"])}", "{str(i["prices"])}"')
                count = count+1
                results.append(i)

        f.close()

        result = f'Se encontraron {count} resultados de la busqueda "{message_og}"'
        print(result)

        search_res = {'product': results}
        return pb2.SearchResults(**search_res)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_SearchServicer_to_server(SearchService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
