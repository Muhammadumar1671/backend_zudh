from logging import exception
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated
from .models import *
import stripe
import os




@api_view(['GET'])
def get_fabric(request):
    fabric = fabric.objects.all()
    return Response(fabric, status=status.HTTP_200_OK)
@api_view(['GET'])
def get_front_type(request):
    front_type = front_type.objects.all()
    return Response(front_type, status=status.HTTP_200_OK)
@api_view(['GET'])
def get_collar_type(request):
    collar_type = collar_type.objects.all()
    return Response(collar_type, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_sleeves_type(request):
    sleeves_type = sleeves_type.objects.all()
    return Response(sleeves_type, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_pockets_type(request):
    pockets_type = pockets_type.objects.all()
    return Response(pockets_type, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_mobile_pocket(request):
    mobile_pocket = mobile_pocket.objects.all()
    return Response(mobile_pocket, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_mobile_pocket_type(request):
    mobile_pocket_type = mobile_pocket_type.objects.all()
    return Response(mobile_pocket_type, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_suit(request):
    fabric_name = request.data.get('fabric_name')
    front_type_name = request.data.get('front_type_name')
    collar_type_name = request.data.get('collar_type_name')
    sleeves_type_name = request.data.get('sleeves_type_name')
    pockets_type_name = request.data.get('pockets_type_name')
    mobile_pocket_name = request.data.get('mobile_pocket_name')
    mobile_pocket_type_name = request.data.get('mobile_pocket_type_name')
    if mobile_pocket_type_name == 'pen':
        pocket_type_required = True
    elif mobile_pocket_type_name == 'mobile':
        number_of_pockets = 1  
    instructions = request.data.get('instructions')
    fabric_price = fabric.objects.get(fabric_color=fabric_name).fabric_price
    front_type_price = front_type.objects.get(front_type_name=front_type_name).front_type_price
    collar_type_price = collar_type.objects.get(collar_type_name=collar_type_name).collar_type_price
    sleeves_type_price = sleeves_type.objects.get(sleeves_type_name=sleeves_type_name).sleeves_type_price
    pockets_type_price = pockets_type.objects.get(pockets_type_name=pockets_type_name).pockets_type_price
    mobile_pocket_price = mobile_pocket_type.objects.get(mobile_pocket_type_name=mobile_pocket_name).mobile_pocket_type_price
    total_price = fabric_price + front_type_price + collar_type_price + sleeves_type_price + pockets_type_price + mobile_pocket_price
    create_suit = suit_details.objects.create(
        fabric=fabric.objects.get(fabric_color=fabric_name),
        front_type=front_type.objects.get(front_type_name=front_type_name),
        collar_type=collar_type.objects.get(collar_type_name=collar_type_name),
        sleeves_type=sleeves_type.objects.get(sleeves_type_name=sleeves_type_name),
        pockets_type=pockets_type.objects.get(pockets_type_name=pockets_type_name),
        mobile_pocket=mobile_pocket.objects.get(mobile_pocket_name=mobile_pocket_name),
        instructions=instructions,
        total_price=total_price
    )
    create_suit.save()
    print(create_suit)
    print(total_price)
    return Response({'message': 'Suit created successfully' , 'id': create_suit.pk}, status=status.HTTP_201_CREATED)



@api_view(['GET'])
@permission_classes([AllowAny])
def cart(request):
    try:
        user = request.data.get('user')
        suit = suit_details.objects.filter(user=user)
        return Response(suit, status=status.HTTP_200_OK)
    except exception as e:
        return Response({'message': 'No user cart found'}, status=status.HTTP_404_NOT_FOUND)