from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Ad, AdAnalytics
from .serializers import AdSerializer
from rest_framework import views
from django.utils import timezone


# Crud operations on Ads performed by the merchant!

class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Optionally restricts the returned ads to the current user,
        by filtering against a `user` query parameter.
        """
        user = self.request.user
        return Ad.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Create analytics from here. PRovide just the ad and playtime total
class TrackAnalyticsView(views.APIView):
    def post(self, request, *args, **kwargs):
        ad_id = request.data.get('ad')
        playtime = request.data.get('playtime')
        try:
            ad = Ad.objects.get(id=ad_id)
            analytics, created = AdAnalytics.objects.get_or_create(ad=ad)
            analytics.update_monthly_data(float(playtime), timezone.now())
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except Ad.DoesNotExist:
            return Response({'error': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)
        

# Gets only for the month specified. FOrmat: ?month=YYYY-mm
class GetMonthlyPlaytimeView(views.APIView):
    def get(self, request, ad_id, *args, **kwargs):
        month = request.query_params.get('month')
        
        try:
            ad = Ad.objects.get(id=ad_id)
            
            if ad.user != request.user:
                return Response({'error': 'You do not have permission to access this ad'}, status=status.HTTP_403_FORBIDDEN)
            
            # Check if the ad has analytics data
            if not hasattr(ad, 'analytics') or ad.analytics.monthly_playtime is None:
                return Response({'error': 'Analytics data not found for this ad'}, status=status.HTTP_404_NOT_FOUND)

            analytics = ad.analytics
            
            if month:
                playtime = analytics.get_monthly_playtime(month)
                if playtime is None:
                    return Response({'error': 'No playtime data available for the specified month'}, status=status.HTTP_404_NOT_FOUND)
                data = {
                    'month': month,
                    'playtime': playtime  # Playtime in seconds
                }
            else:
                data = {
                    'error': 'Month parameter is required'
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(data, status=status.HTTP_200_OK)

        except Ad.DoesNotExist:
            return Response({'error': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)


# gets data for all months in this itself

class GetAllMonthlyPlaytimeView(views.APIView):
    def get(self, request, ad_id, *args, **kwargs):
        try:
            # Retrieve the ad object
            ad = Ad.objects.get(id=ad_id)
            
            # Check if the ad belongs to the current user
            if ad.user != request.user:
                return Response({'error': 'You do not have permission to access this ad'}, status=status.HTTP_403_FORBIDDEN)
            
            # Retrieve monthly playtime data
            if not hasattr(ad, 'analytics') or ad.analytics.monthly_playtime is None:
                return Response({'error': 'Analytics data not found'}, status=status.HTTP_404_NOT_FOUND)
            
            monthly_playtime = ad.analytics.monthly_playtime  # Get the playtime data
            
            # Prepare the response data
            data = {
                'ad_id': ad_id,
                'monthly_playtime': monthly_playtime
            }
            return Response(data, status=status.HTTP_200_OK)
        
        except Ad.DoesNotExist:
            return Response({'error': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)
