from django.db import models

from django.db import models

class Country(models.Model):
    # l'identifiant unique cca3 avec une clé primaire
    cca3 = models.CharField(max_length=3, primary_key=True)
    
    # Info de Base
    name = models.CharField(max_length=200) 
    cca2 = models.CharField(max_length=2, null=True, blank=True)
    capital = models.CharField(max_length=200, null=True, blank=True)
    
    # Info geographique region et sous_region
    region = models.CharField(max_length=100)
    subregion = models.CharField(max_length=100, null=True, blank=True)
    
    # Données chiffrées 
    population = models.BigIntegerField(default=0) #( en big int car la population depasse lemilliard)
    area = models.FloatField(default=0.0)
    
    # URL du drapeau (le lien vers l image)
    flag_url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.cca3})"
