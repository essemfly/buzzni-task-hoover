from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from hoover.models import Hoover
from hoover.serializers import HooverSerializer


class HooverSearch(APIView):
    def get(self, request, format=None):
        keyword = request.query_params.get('keyword', None)
        hoovers = Hoover.objects.all().order_by('-avg_rating')[:5]
        serializer = HooverSerializer(hoovers, many=True)
        return Response(serializer.data)


class HooverList(APIView):
    def get(self, request, format=None):
        hoovers = Hoover.objects.all()
        serializer = HooverSerializer(hoovers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = HooverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HooverDetail(APIView):
    def get_object(self, pk):
        try:
            return Hoover.objects.get(pk=pk)
        except Hoover.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        hoover = self.get_object(pk)
        serializer = HooverSerializer(hoover)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        hoover = self.get_object(pk)
        serializer = HooverSerializer(hoover, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        hoover = self.get_object(pk)
        hoover.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)