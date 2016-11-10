from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from hoover.models import Hoover
from hoover.serializers import HooverSerializer
from hoover import analyzer
from operator import itemgetter


class HooverSearch(APIView):
    def get(self, request, format=None):
        search_input = request.query_params.get('keyword', None)

        if search_input:
            keywords = analyzer.get_keyword(search_input)

            # 모든 Reviews 들에 대해 단어를 검색해서 사용할 경우 -> 예전에 사용
            # hoover_scores = analyzer.get_recommended_hoover(keywords)

            # Elastic Search를 이용한 검색을 할 경우!
            hoover_scores = analyzer.get_recommended_hoover_by_dict(keywords)

            sorted_hoover_scores = sorted(hoover_scores.items(), key=itemgetter(1), reverse=True)
            sorted_hoover_ids = []
            for sorted_hoover in sorted_hoover_scores:
                sorted_hoover_ids.append(sorted_hoover[0])
            unsorted_hoovers = Hoover.objects.in_bulk(sorted_hoover_ids)
            hoovers = [unsorted_hoovers[hoover_id] for hoover_id in sorted_hoover_ids]
        else:
            hoovers = Hoover.objects.all()[:20]

        serializer = HooverSerializer(hoovers[:20], many=True)
        return Response(serializer.data)


class HooverList(APIView):
    def get(self, request, format=None):
        hoovers = Hoover.objects.all()[:20]
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