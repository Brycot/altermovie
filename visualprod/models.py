"""
    Models VisualProd
"""

from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User

# Create your models here.


class VisualProd(models.Model):
    """
        Model Representing a audiovisual producction
    """
    name = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    TYPE_CHOICES = [
        ('Movie', 'Movie'),
        ('Serie', 'Serie'),
    ]
    type = models.CharField(
        max_length=5,
        choices=TYPE_CHOICES
    )
    number_visualizations = models.IntegerField(default=0)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.name + ' - ' + self.genre + ' - ' + self.type + ' - ' + str(self.rating)


class UserInteraction(models.Model):
    """
        Model Representing a interacction of user with a audiovisual producction
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visual_prod = models.ForeignKey(VisualProd, on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)
    rating = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username + ' - ' + self.visual_prod.name + ' - ' + str(self.viewed) + ' - ' + str(self.rating)

    class Meta:
        unique_together = ('user', 'visual_prod')
