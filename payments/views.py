
from django.shortcuts import redirect, render
import stripe
from dotenv import load_dotenv
import os
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from suit.models import suit_details
from django.http import HttpResponse
from django.http import JsonResponse


load_dotenv()

@api_view(['GET'])
@permission_classes([AllowAny])
def stripe_checkout_page(request):
    return  render(request, 'stripe/stripe_checkout.html')

@api_view(['POST'])
@permission_classes([AllowAny])
def create_checkout_session(request):
    suit_price = 1000
    stripe.api_key = os.environ.get('STRIPE_API_KEY')
    print(stripe.api_key)
    
    try:
        # Create a Product
        product = stripe.Product.create(
            name="Suit",
            description="User generated suit",
        )
        
        # Create a Price for the Product
        price = stripe.Price.create(
            unit_amount=suit_price,
            currency='aed',
            product=product.id,
        )
        
        # Create a Checkout Session
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': price.id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://localhost:8000/payment/success?success=true',
            cancel_url='http://localhost:8000/payment/unsuccessful?canceled=true',
        )
        
        return redirect(checkout_session.url, code=303)
    
    except Exception as e:
        # Return a JSON response with the error message and status code 400 (Bad Request)
        return JsonResponse({'error': str(e)}, status=400)


def payment_success(request):
    return HttpResponse({'message': 'Payment successful'}, status=status.HTTP_200_OK)

def payment_cancel(request):
    return HttpResponse({'message': 'Payment canceled'}, status=status.HTTP_400_BAD_REQUEST)