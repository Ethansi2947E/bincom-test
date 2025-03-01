from django.shortcuts import render
from django.db.models import Sum
from django.contrib import messages
from .models import PollingUnit, AnnouncedPuResults, LGA
from django.utils import timezone
from django.db import transaction

def polling_unit_result(request):
    """Display results for a specific polling unit."""
    polling_units = PollingUnit.objects.all()
    results = None
    selected_unit = None

    if 'polling_unit' in request.GET and request.GET.get('polling_unit'):  # Only proceed if polling_unit has a value
        unit_id = request.GET.get('polling_unit')
        try:
            selected_unit = PollingUnit.objects.get(uniqueid=unit_id)
            results = AnnouncedPuResults.objects.filter(polling_unit=unit_id)
        except PollingUnit.DoesNotExist:
            messages.error(request, 'Polling unit not found')

    context = {
        'polling_units': polling_units,
        'results': results,
        'selected_unit': selected_unit
    }
    return render(request, 'election_results/polling_unit_result.html', context)

def lga_result(request):
    """Display summed results for all polling units in an LGA."""
    lgas = LGA.objects.all()
    results = None
    selected_lga = None
    total_score = 0

    if 'lga' in request.GET:
        lga_id = request.GET.get('lga')
        try:
            selected_lga = LGA.objects.get(lga_id=lga_id)
            # Get all polling units in the LGA
            polling_units = PollingUnit.objects.filter(lga=lga_id)
            # Get results for all polling units and group by party
            results = AnnouncedPuResults.objects.filter(
                polling_unit__in=polling_units.values_list('uniqueid', flat=True)
            ).values('party_abbreviation').annotate(
                total_score=Sum('party_score')
            ).order_by('party_abbreviation')
            
            # Calculate total votes
            total_score = sum(result['total_score'] for result in results)
        except LGA.DoesNotExist:
            messages.error(request, 'LGA not found')

    context = {
        'lgas': lgas,
        'results': results,
        'selected_lga': selected_lga,
        'total_score': total_score
    }
    return render(request, 'election_results/lga_result.html', context)

def store_result(request):
    """Store results for a new polling unit."""
    lgas = LGA.objects.all()
    parties = ['PDP', 'DPP', 'ACN', 'PPA', 'CDC', 'JP']  # Add all relevant parties
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Create new polling unit
                polling_unit = PollingUnit.objects.create(
                    ward_id=request.POST.get('ward'),
                    lga_id=request.POST.get('lga'),
                    uniqueid=PollingUnit.objects.all().order_by('-uniqueid').first().uniqueid + 1,
                    polling_unit_number=request.POST.get('polling_unit_number'),
                    polling_unit_name=request.POST.get('polling_unit_name'),
                    polling_unit_description=request.POST.get('polling_unit_description'),
                    lat=request.POST.get('latitude'),
                    long=request.POST.get('longitude'),
                    entered_by_user=request.POST.get('entered_by'),
                    user_ip_address=request.META.get('REMOTE_ADDR')
                )

                # Store results for each party
                for party in parties:
                    score = request.POST.get(f'party_{party}', 0)
                    if score:
                        AnnouncedPuResults.objects.create(
                            polling_unit=polling_unit,
                            party_abbreviation=party,
                            party_score=int(score),
                            entered_by_user=request.POST.get('entered_by'),
                            user_ip_address=request.META.get('REMOTE_ADDR')
                        )

                messages.success(request, 'Results stored successfully!')
        except Exception as e:
            messages.error(request, f'Error storing results: {str(e)}')

    context = {
        'lgas': lgas,
        'parties': parties
    }
    return render(request, 'election_results/store_result.html', context)
