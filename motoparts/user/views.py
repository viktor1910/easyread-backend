from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserReadSerializer, UserLoginSerializer
from .permissions import IsAdminUser

# Create your views here.

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        import sys
        sys.stdout.write(f"\n\nRegistration data received: {request.data}\n\n")
        sys.stdout.flush()

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            user_data = UserReadSerializer(user).data
            return Response({
                'message': 'User registered successfully',
                'user': user_data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)

        sys.stdout.write(f"\n\nValidation errors: {serializer.errors}\n\n")
        sys.stdout.flush()
        return Response({
            'message': 'Registration failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def user_list(request):
    """Get all users - Admin only"""
    users = CustomUser.objects.all()
    serializer = UserReadSerializer(users, many=True)
    return Response(serializer.data)

class UserLoginView(generics.GenericAPIView):
    """User login endpoint that returns authentication token"""
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            user_data = UserReadSerializer(user).data
            
            return Response({
                'message': 'Login successful',
                'token': token.key,
                'user': user_data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'message': 'Login failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """User logout endpoint that removes authentication token"""
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({
            'message': 'User was not logged in'
        }, status=status.HTTP_400_BAD_REQUEST)
