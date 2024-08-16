from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login
from .serializers import RegisterSerializer, LoginSerializer
from django.middleware.csrf import get_token
from django.http import JsonResponse
from .models import AdPreferences
from .serializers import AdPreferencesSerializer
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])  # Allow any user to register
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])  # Allow any user to login
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])  # Allow any user to access this endpoint
def csrf_token_view(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])  # Allow any user to access this test endpoint
def test_view(request):
    return JsonResponse({'message': 'This is a test endpoint.'})

@csrf_exempt

@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def ad_preferences(request):
    try:
        ad_preferences = AdPreferences.objects.get(user=request.user)
    except AdPreferences.DoesNotExist:
        if request.method == 'GET':
            return Response({"error": "Ad preferences not found."}, status=status.HTTP_404_NOT_FOUND)
        elif request.method in ['PUT', 'PATCH']:
            # Optionally, you could create a new AdPreferences instance if it doesn't exist,
            # but typically you would only allow updates to existing records.
            return Response({"error": "Ad preferences not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AdPreferencesSerializer(ad_preferences)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method in ['PUT', 'PATCH']:
        serializer = AdPreferencesSerializer(ad_preferences, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
