from django.db import models
from users.models import CustomUser
from django.utils import timezone
from datetime import datetime

class Gender(models.Model):
    value = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.value

class TimeOfDay(models.Model):
    value = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.value

class AgeRange(models.Model):
    value = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.value


class Ad(models.Model):
    TYPE_CHOICES = [
        ('specific', 'Specific'),
        ('generic', 'Generic'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.URLField(max_length=2000)
    age_range = models.ManyToManyField(AgeRange, blank=True)
    location = models.CharField(max_length=255)
    gender = models.ManyToManyField(Gender, blank=True)
    time_of_day = models.ManyToManyField(TimeOfDay, blank=True)
    maximum_budget = models.IntegerField()
    category = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    ad_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='generic',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} from {self.user.name}"
    

# Budget for the user for one ad only!!!
class Budget(models.Model):
    ad = models.OneToOneField(Ad, on_delete=models.CASCADE)
    advertiser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_budget = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Ensure default value

    def save(self, *args, **kwargs):
        if not self.remaining_budget:
            self.remaining_budget = self.total_budget  # Set remaining_budget to total_budget if not provided
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ad.title} budget"


# Spending history of that user for analytics and other purpose we can use.
class SpendingHistory(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='spending_history')
    date = models.DateField()
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_budget = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Spending on {self.date} for {self.budget.ad.title}"


# Analytics below
class AdAnalytics(models.Model):
    ad = models.OneToOneField(Ad, on_delete=models.CASCADE, related_name='analytics')
    total_playtime = models.FloatField(default=0)  # Total playtime in seconds
    monthly_playtime = models.JSONField(default=dict)  # Store playtime by month
    last_played_at = models.DateTimeField(null=True, blank=True)

    def update_monthly_data(self, playtime, timestamp):
        month_key = timestamp.strftime('%Y-%m')
        if month_key in self.monthly_playtime:
            self.monthly_playtime[month_key] += playtime
        else:
            self.monthly_playtime[month_key] = playtime
        
        self.total_playtime += playtime
        self.last_played_at = timestamp
        self.save()

    def get_monthly_playtime(self, month):
        return self.monthly_playtime.get(month, 0)  # Return playtime in seconds

    def __str__(self):
        return f"Analytics for Ad: {self.ad.title}"