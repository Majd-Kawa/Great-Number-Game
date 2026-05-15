from django.db import models

# Create your models here.
class LeaderboardScore(models.Model):
    player_name = models.CharField(max_length=100)
    attempts = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player_name} - {self.attempts}"