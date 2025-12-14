from django.db import models
from artists.models import Group, SoloArtist #importer des données depuis l'application artists

class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('release', 'Release'),
        ('event', 'Event'),
        ('birthday', 'Birthday/Anniversary')
    ]

    title = models.CharField(max_length=255)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    date = models.DateField('Date')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, related_name='group_events')
    solo_artist = models.ForeignKey(SoloArtist, on_delete=models.CASCADE, null=True, blank=True, related_name='solo_events')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        artist = self.group.name if self.group else (self.solo_artist.stage_name if self.solo_artist else 'No artist')
        return f'{self.title} - {artist} ({self.date})'

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['date']