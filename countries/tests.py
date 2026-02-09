from django.test import TestCase
from django.urls import reverse
from .models import Country

class CountryModelTest(TestCase):
    def setUp(self):
        # Une méthode qui s'execute avent chaque test
        # On crée un faux pays pour tester.
        Country.objects.create(
            cca3='DZA',
            name='Algeria',
            population=44000000,
            region='Africa'
        )

    def test_country_creation(self):
        # On vérifie que le pays a bien été créé dans la base de test
        algeria = Country.objects.get(cca3='DZA')
        self.assertEqual(algeria.name, 'Algeria')
        self.assertEqual(algeria.population, 44000000)

class CountryViewTest(TestCase):
    def setUp(self):
        # On recrée le pays car la base est nettoyée entre chaque test
        Country.objects.create(
            cca3='FRA',
            name='France',
            region='Europe'
        )

    def test_view_url_exists_at_desired_location(self):
        
        # On teste si l'URL /countries/ répond bien (Code 200 = OK)
        response = self.client.get('/countries/')
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):

        # On teste si la vue utilise bien le bon fichier HTML
        response = self.client.get('/countries/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'countries/country_list.html')
        


    def test_detail_page(self):
        # On teste si la page détail fonctionne pour la France
        response = self.client.get('/countries/FRA/')
        self.assertEqual(response.status_code, 200)
        # On vérifie que le mot "France" est bien écrit sur la page
        self.assertContains(response, "France")