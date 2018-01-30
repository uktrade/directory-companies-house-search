from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from directory_healthcheck.views import BaseHealthCheckAPIView
from health_check.db.backends import DatabaseBackend
from health_check.cache.backends import CacheBackend

from chsearch.signature import SignatureCheckPermission
from healthcheck.backends import ElasticSearchCheckBackend



class DatabaseAPIView(BaseHealthCheckAPIView):
    def create_service_checker(self):
        return DatabaseBackend()


class CacheAPIView(BaseHealthCheckAPIView):
    def create_service_checker(self):
        return CacheBackend()


class ElasticsearchAPIView(BaseHealthCheckAPIView):
    def create_service_checker(self):
        return ElasticSearchCheckBackend()


class PingAPIView(APIView):

    permission_classes = (SignatureCheckPermission, )
    http_method_names = ("get", )

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)
