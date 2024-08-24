
from oauthlib.common import generate_token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import User_Model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    

    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')
    if (User_Model.objects.filter(email=email).exists()):
        return Response({'message': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    password = request.data.get('password')
    phone_number = request.data.get('phone_number')
    country = request.data.get('country')
    create_user = User_Model.objects.create_user(
        first_name=first_name, 
        last_name=last_name, 
        email=email, 
        password=password, 
        phone_number=phone_number, 
        country=country
    )
    print(create_user)
    create_user.save()

    return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User_Model.objects.get(email=email)
    except User_Model.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if user.check_password(password):
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Login failed. Check your credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

def verify_jwt_token(token):
    try:
        # Decode the token
        access_token = AccessToken(token)
        # You can access token claims if needed
        user_id = access_token['user_id']
        # Do something with the user_id or other claims
        return True, user_id
    except TokenError as e:
        # Token is invalid or expired
        return False, str(e)

# Example usage in a view
@api_view(['GET'])
def check_token(request):
    token = request.headers.get('Authorization', '').split(' ')[-1]  # Extract token from Authorization header
    is_valid, result = verify_jwt_token(token)
    
    if is_valid:
        return Response({'message': 'Token is valid', 'user_id': result}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Token is invalid', 'error': result}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_endpoint(request):
    return Response({'message': 'This is a protected endpoint'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def logout(request):
    try:
        # Extract the refresh token from the request data
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a RefreshToken instance and blacklist it
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)