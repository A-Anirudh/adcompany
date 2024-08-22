from rest_framework import serializers
from .models import Ad,Budget, SpendingHistory,AgeRange,Gender,TimeOfDay


class AdSerializer(serializers.ModelSerializer):
    age_range = serializers.PrimaryKeyRelatedField(many=True, queryset=AgeRange.objects.all())
    gender = serializers.PrimaryKeyRelatedField(many=True, queryset=Gender.objects.all())
    time_of_day = serializers.PrimaryKeyRelatedField(many=True, queryset=TimeOfDay.objects.all())

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ad
        fields = '__all__'

    def create(self, validated_data):
        # The user is automatically set by HiddenField
        age_ranges = validated_data.pop('age_range')
        genders = validated_data.pop('gender')
        times_of_day = validated_data.pop('time_of_day')
        
        ad = Ad.objects.create(**validated_data)
        ad.age_range.set(age_ranges)
        ad.gender.set(genders)
        ad.time_of_day.set(times_of_day)
        return ad
    

class BudgetSerializer(serializers.ModelSerializer):
    advertiser_name = serializers.CharField(source='advertiser.name', read_only=True)
    ad_title = serializers.CharField(source='ad.title', read_only=True)

    class Meta:
        model = Budget
        fields = ['id', 'ad', 'ad_title', 'advertiser', 'advertiser_name', 'total_budget', 'remaining_budget']
        read_only_fields = ['remaining_budget', 'last_updated']

    def __str__(self):
        return f"Budget for {self.ad_title} by {self.advertiser_name}"

class SpendingHistorySerializer(serializers.ModelSerializer):
    ad_title = serializers.CharField(source='budget.ad.title', read_only=True)
    advertiser_name = serializers.CharField(source='budget.advertiser.name', read_only=True)

    class Meta:
        model = SpendingHistory
        fields = ['id', 'budget', 'ad_title', 'advertiser_name', 'date', 'amount_spent', 'remaining_budget', 'updated_at']
        read_only_fields = ['remaining_budget', 'updated_at']

    def __str__(self):
        return f"Spending on {self.date} for {self.ad_title}"
