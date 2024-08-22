from django.http import JsonResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Ad, AdAnalytics, Budget
from .serializers import AdSerializer,BudgetSerializer
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def ad_operations(request, ad_id=None):
    user = request.user
    print('request came through', user, request.user)

    # GET method for retrieving ads
    if request.method == 'GET':
        if ad_id:
            try:
                ad = Ad.objects.get(id=ad_id, user=user)
                serializer = AdSerializer(ad)
                return JsonResponse(serializer.data, safe=False)
            except Ad.DoesNotExist:
                return JsonResponse({'error': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            ads = Ad.objects.filter(user=user)
            serializer = AdSerializer(ads, many=True)
            return JsonResponse(serializer.data, safe=False)

    # POST method for creating a new ad and budget
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        ad_serializer = AdSerializer(data=data, context={'request': request})

        if ad_serializer.is_valid():
            ad = ad_serializer.save()
            if 'total_budget' in data:
                budget_data = {
                    'ad': ad.id,
                    'advertiser': user.id,
                    'total_budget': data['total_budget'],
                    'remaining_budget': data['total_budget']  # Set the initial remaining_budget
                }
                budget_serializer = BudgetSerializer(data=budget_data)
                if budget_serializer.is_valid():
                    budget_serializer.save()
                else:
                    ad.delete()
                    return JsonResponse(budget_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return JsonResponse(ad_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(ad_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        if not ad_id:
            return JsonResponse({'error': 'Ad ID is required for updating'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ad = Ad.objects.get(id=ad_id, user=user)
            budget = Budget.objects.get(ad=ad)
            data = JSONParser().parse(request)
            ad_serializer = AdSerializer(ad, data=data, partial=True)
            if ad_serializer.is_valid():
                ad_serializer.save()
                if 'total_budget' in data:
                    total_budget = data.get('total_budget')
                    budget.remaining_budget += (total_budget - budget.total_budget)  # Adjust the remaining budget
                    budget.total_budget = total_budget
                    budget_serializer = BudgetSerializer(budget, partial=True)
                    if budget_serializer.is_valid():
                        budget_serializer.save()
                    else:
                        return JsonResponse(budget_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return JsonResponse(ad_serializer.data, status=status.HTTP_200_OK)
            return JsonResponse(ad_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Ad.DoesNotExist:
            return JsonResponse({'error': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)
        except Budget.DoesNotExist:
            return JsonResponse({'error': 'Budget not found'}, status=status.HTTP_404_NOT_FOUND)
    # DELETE method for deleting an ad
    elif request.method == 'DELETE':
        if not ad_id:
            return JsonResponse({'error': 'Ad ID is required for deletion'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            ad = Ad.objects.get(id=ad_id, user=user)
            ad.delete()
            return JsonResponse({'message': 'Ad deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Ad.DoesNotExist:
            return JsonResponse({'error': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)
        

# Track analytics for an ad
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def track_analytics(request):
    ad_id = request.data.get('ad')
    playtime = request.data.get('playtime')

    try:
        ad = Ad.objects.get(id=ad_id)
        if ad.user != request.user:
            return Response({'error': 'You do not have permission to access this ad'}, status=status.HTTP_403_FORBIDDEN)

        analytics, created = AdAnalytics.objects.get_or_create(ad=ad)
        analytics.update_monthly_data(float(playtime), timezone.now())
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
    except Ad.DoesNotExist:
        return Response({'error': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)


# Get monthly playtime for a specific ad
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_monthly_playtime(request, ad_id):
    month = request.GET.get('month')

    try:
        ad = Ad.objects.get(id=ad_id)
        if ad.user != request.user:
            return Response({'error': 'You do not have permission to access this ad'}, status=status.HTTP_403_FORBIDDEN)

        analytics = ad.analytics
        if not hasattr(analytics, 'monthly_playtime') or analytics.monthly_playtime is None:
            return Response({'error': 'Analytics data not found for this ad'}, status=status.HTTP_404_NOT_FOUND)

        if month:
            playtime = analytics.get_monthly_playtime(month)
            if playtime is None:
                return Response({'error': 'No playtime data available for the specified month'}, status=status.HTTP_404_NOT_FOUND)
            data = {
                'month': month,
                'playtime': playtime  # Playtime in seconds
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Month parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    except Ad.DoesNotExist:
        return Response({'error': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)

# Get all monthly playtime for a specific ad
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_monthly_playtime(request, ad_id):
    try:
        ad = Ad.objects.get(id=ad_id)
        if ad.user != request.user:
            return Response({'error': 'You do not have permission to access this ad'}, status=status.HTTP_403_FORBIDDEN)

        analytics = ad.analytics
        if not hasattr(analytics, 'monthly_playtime') or analytics.monthly_playtime is None:
            return Response({'error': 'Analytics data not found for this ad'}, status=status.HTTP_404_NOT_FOUND)

        monthly_playtime = analytics.monthly_playtime  # Get the playtime data
        data = {
            'ad_id': ad_id,
            'monthly_playtime': monthly_playtime
        }
        return Response(data, status=status.HTTP_200_OK)

    except Ad.DoesNotExist:
        return Response({'error': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)
