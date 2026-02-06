from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count
from .models import Country

def country_list(request):
    countries = Country.objects.all().order_by('name')
    
    # On récupère les filtres envoyés par le formulaire 
    search_query = request.GET.get('q', '')      # Recherche par nom
    region_filter = request.GET.get('region', '') # Filtre par région


    if search_query:
        # Remarque:'icontains' veut dire "contient le texte" (elle est insensible aux majuscules/minuscules)
        countries = countries.filter(name__icontains=search_query)
    
    if region_filter:
        countries = countries.filter(region=region_filter)

    # (Optionnel) Pour remplir la liste déroulante des régions automatiquement
    # On cherche toutes les régions uniques qui existent dans la base
    regions_list = Country.objects.values_list('region', flat=True).distinct().order_by('region')

    # Pagination 
    paginator = Paginator(countries, 50) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'regions_list': regions_list,
        'current_search': search_query,
        'current_region': region_filter,
    }
    return render(request, 'countries/country_list.html', context)

def country_detail(request, cca3):
    country = get_object_or_404(Country, pk=cca3)
    context = {'country': country}
    return render(request, 'countries/country_detail.html', context)

def stats_view(request):
    # Nombre total de pays avec COUNt
    total_countries = Country.objects.count()

    # Top 10 par Population ( '-' du plus grand au plus petit) seulement les 10ers
    top_population = Country.objects.all().order_by('-population')[:10]
    # Top 10 par superficie 
    top_area = Country.objects.all().order_by('-area')[:10]

    # par Région
    # On groupe par region et on compte combien il y a de pays dans chaque groupe
    regions_distribution = Country.objects.values('region').annotate(total=Count('region')).order_by('-total')

    context = {
        'total_countries': total_countries,
        'top_population': top_population,
        'top_area': top_area,
        'regions_distribution': regions_distribution,
    }
    return render(request, 'countries/stats.html', context)