from django.db import models


class Attractions(models.Model):
    name = models.CharField(max_length=30)
    text = models.TextField(max_length=1000, default='')
    wikipedia = models.URLField(blank=True)
    tripadvisor = models.URLField(blank=True)
    google_map = models.URLField(blank=True)
    web_site = models.URLField(blank=True)
    image = models.ImageField(blank=True, default='no_image.png')

    def publish(self):
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
