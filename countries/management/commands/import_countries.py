import requests
from django.core.management.base import BaseCommand
from countries.models import Country

class Command(BaseCommand):
    help = 'Importe les données depuis l\'API RestCountries vers la base de données locale'

    def handle(self, *args, **kwargs):
        self.stdout.write("Démarrage de l'importation...")

        # L'URL de l'API 
        url = "https://restcountries.com/v3.1/all?fields=name,cca2,cca3,capital,region,subregion,population,area,flags"

        response = requests.get(url)
        
        # Si l'API ne répond pas code 200, on arrête tout
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR('Erreur lors de l\'appel API'))
            return

        # Parsing JSON pour la récup de données
        countries_data = response.json()
        self.stdout.write(f"{len(countries_data)} pays trouvés. Insertion en base...")

        #On traite chaque pays un par un
        count = 0
        for item in countries_data:
            # on nettoie les données, si pas de capitale on met None
            capital_value = item.get('capital', [None])[0] if item.get('capital') else None
          
            flag_value = item.get('flags', {}).get('svg', '')

            # Sauvegarde en Base de données
            # update ou create, si CCA3 existe déja faut seulement mettre à jour pour eviter les doublons, si pas de CCA3, il va le créer
        
            country, created = Country.objects.update_or_create(
                cca3=item['cca3'], 
                defaults={
                    'name': item['name']['common'],
                    'cca2': item['cca2'],
                    'capital': capital_value,
                    'region': item['region'],
                    'subregion': item.get('subregion', ''),
                    'population': item['population'],
                    'area': item['area'],
                    'flag_url': flag_value
                }
            )
            count += 1
            
            # Petite barre de progression simples
            if count % 10 == 0:
                self.stdout.write(f"Traité : {count} pays...", ending='\r')

        self.stdout.write(self.style.SUCCESS(f'Succès ! {count} pays importés ou mis à jour.'))