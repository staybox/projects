from django.db import models
from django.core.validators import RegexValidator

class Attractions(models.Model):
    name = models.CharField(max_length=30)
    text = models.TextField(max_length=1000, default='')
    wikipedia = models.URLField(blank=True)
    tripadvisor = models.URLField(blank=True)
    google_map = models.URLField(blank=True)
    web_site = models.URLField(blank=True)
    town = models.CharField(max_length=30, blank=True, default='')
    image = models.ImageField(blank=True, default='no_image.png')
    image_map = models.ImageField(blank=True, default='no_image.png')

    def publish(self):
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Towns(models.Model):
    name = models.CharField(max_length=25)
    text = models.TextField(max_length=1000, default='')
    wikipedia = models.URLField(blank=True)
    tripadvisor = models.URLField(blank=True)
    google_map = models.URLField(blank=True)
    image = models.ImageField(blank=True, default='no_image.png')
    image_map = models.ImageField(blank=True, default='no_image.png')

    def publish(self):
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Orders(models.Model):
    client_name = models.CharField(max_length=25, blank=True, default='')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+x xxx xxx xx xx'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=False)
    order = models.CharField(max_length=200, blank=False)
    order_date = models.DateTimeField(auto_now_add=True, blank=False)

    def publish(self):
        self.save()

    def __str__(self):
        return self.client_name

    class Meta:
        ordering = ['client_name']