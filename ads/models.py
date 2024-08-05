from django.db import models
from users.models import CustomUser
from django.utils import timezone

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
        return f"{self.title} from {self.user.first_name}"


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
