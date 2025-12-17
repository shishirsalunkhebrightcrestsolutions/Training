from django.shortcuts import render
from .models import Transactions
from rest_framework.response import Response
from .serializers import TransactionsSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.db.models import Sum
# Create your views here.

@api_view()
def get_transactions (request):
    queryset= Transactions.objects.all().order_by("-pk")
    serializer=TransactionsSerializer(queryset, many=True)
    return Response({
        "data" : serializer.data,
        "total": queryset.aggregate(total=Sum('amount'))['total'] or 0
    })


class TransactionAPI(APIView):
    def get(self,request):
        queryset= Transactions.objects.all().order_by("-pk")
        serializer=TransactionsSerializer(queryset, many=True)
        return Response({
            "data" : serializer.data,
            "total": queryset.aggregate(total=Sum('amount'))['total'] or 0
        })

    def post(self,request):
        data=request.data
        serializer=TransactionsSerializer(data=data)
        if not serializer.is_valid():
            return Response ({
                "message":"data not saved",
                "errors":serializer.errors,
            })
        serializer.save ()
        return Response({
            "message": "data save ",
            "data":serializer.data
        })

    def put(self,request):
        return Response({
            "message": "this is a put method"
        })

    def patch(self,request):
        data=request.data
        if not data.get('id'):
             return Response ({
                "message":"data not updated",
                "errors":"id is required",
            })

        transaction= Transactions.objects.get(id=data.get('id'))
        serializer= TransactionsSerializer(
             transaction, data=data, partial=True )
        
        if not serializer.is_valid():
            return Response ({
                "message":"data not saved",
                "errors":serializer.errors,
            })
        serializer.save ()
        return Response({
            "message": "data save ",
            "data":serializer.data
        })

       
    def delete(self,request):
        data=request.data
        if not data.get('id'):
             return Response ({
                "message":"data not updated",
                "errors":"id is required",
            })

        transaction= Transactions.objects.get(id=data.get('id')).delete()
        
       
        return Response({
            "message": "data delete ",
            "data":{}
        })