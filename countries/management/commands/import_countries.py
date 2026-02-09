import requests
from django.core.management.base import BaseCommand
from countries.models import Country
import time




class Command(BaseCommand):
    help = 'Importe les données depuis l\'API RestCountries vers la base de données locale'

    def handle(self, *args, **kwargs):
        self.stdout.write("Démarrage de l'importation avec Retry...")

# L'URL de l'API 
        url = "https://restcountries.com/v3.1/all?fields=name,cca2,cca3,capital,region,subregion,population,area,flags"
        
        #Le  Retry api
        max_retries = 3  
        delay = 2        
        data = None      
#une boucle retry
        for attempt in range(1, max_retries + 1):
            try:
                self.stdout.write(f"Tentative {attempt}/{max_retries}...")
                response = requests.get(url, timeout=10) # timeout=10 pour eviter que ça charge a l infinie
                
                # Si le code est 200 , on sort de la boucle immédiatement
                if response.status_code == 200:
                    data = response.json()
                    self.stdout.write(self.style.SUCCESS("Connexion réussie !"))
                    break 
                else:
                    self.stdout.write(self.style.WARNING(f"Erreur API (Code {response.status_code})..."))
            
            except requests.exceptions.RequestException as e:

                # Si on a une erreur de connexion (coupure internet, DNS...)
                self.stdout.write(self.style.ERROR(f"Erreur de connexion : {e}"))



            # Si on n'a pas réussi et qu'il reste des tentatives, on attend
            if attempt < max_retries:
                self.stdout.write(f"Attente de {delay} secondes avant réessai...")
                time.sleep(delay)
            else:
                # Si c'était la dernière tentative et que ça a raté
                self.stdout.write(self.style.ERROR("Abandon après 3 échecs."))
                return # On arrête tout le script
        


        self.stdout.write(f"{len(data)} pays trouvés. Insertion en base...")

        count = 0
        for item in data:
            capital_value = item.get('capital', [None])[0] if item.get('capital') else None
            flag_value = item.get('flags', {}).get('svg', '')

            Country.objects.update_or_create(
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
            if count % 10 == 0:
                self.stdout.write(f"Traité : {count} pays...", ending='\r')

        self.stdout.write(self.style.SUCCESS(f'Succès ! {count} pays importés ou mis à jour.'))