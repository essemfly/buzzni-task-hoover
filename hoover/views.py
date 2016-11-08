from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from hoover.models import Hoover
from hoover.serializers import HooverSerializer


@api_view(['GET', 'POST'])
def hoover_list(request):
    if request.method == 'GET':
        hoovers = Hoover.objects.all()
        serializer = HooverSerializer(hoovers, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = HooverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def hoover_detail(request, pk):
    try:
        hoover = Hoover.objects.get(pk=pk)
    except Hoover.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = HooverSerializer(hoover)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = HooverSerializer(hoover, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        hoover.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
