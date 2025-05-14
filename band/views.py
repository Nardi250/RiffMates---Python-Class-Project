from django.shortcuts import render,get_object_or_404
from .models import Musician 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required

@login_required
def restricted_page(request):
    data = {
        'title' : 'Restricted Page',
    'content' : '<h1>you are logged in </h1>'
    }
    return render(request, 'general.html', data)

# Create your views here.
def viewBand(request, musician_id):
    musician = get_object_or_404(Musician, pk=musician_id)
    return render(request, 'band/band.html', {'musician': musician})


def viewAllBands(request):
    musicians_list = Musician.objects.all()
    paginator = Paginator(musicians_list, 10) 

    page_number = request.GET.get('page')
    try:
        musicians = paginator.page(page_number)
    except PageNotAnInteger:
        musicians = paginator.page(1)
    except EmptyPage:
        musicians = paginator.page(paginator.num_pages)

    context = {'musicians': musicians}
    return render(request, 'all_bands.html', context)

def viewMusicianDetails(request, id):

    musician = get_object_or_404(Musician, id=id)
    context = {
        'musician': musician
    }
    return render(request, 'musician_detail.html', context)


# views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Musician, Band, Venue

def musician_list(request):
    # Handle per_page parameter
    per_page = request.GET.get('per_page', 10)
    try:
        per_page = int(per_page)
        per_page = min(max(1, per_page), 50)  # Constrain between 1-50
    except ValueError:
        per_page = 10

    musicians_list = Musician.objects.all()
    paginator = Paginator(musicians_list, per_page)
    
    page_number = request.GET.get('page')
    try:
        musicians = paginator.page(page_number)
    except PageNotAnInteger:
        musicians = paginator.page(1)
    except EmptyPage:
        musicians = paginator.page(paginator.num_pages)

    context = {
        'musicians': musicians,
        'per_page': per_page,
    }
    return render(request, 'musician_list.html', context)


# views.py
def band_list(request):
    # Handle per_page parameter
    per_page = request.GET.get('per_page', 10)
    try:
        per_page = int(per_page)
        per_page = min(max(1, per_page), 50)
    except ValueError:
        per_page = 10

    bands_list = Band.objects.all()
    paginator = Paginator(bands_list, per_page)
    
    page_number = request.GET.get('page')
    try:
        bands = paginator.page(page_number)
    except PageNotAnInteger:
        bands = paginator.page(1)
    except EmptyPage:
        bands = paginator.page(paginator.num_pages)

    context = {
        'bands': bands,
        'per_page': per_page,
    }
    return render(request, 'band_list.html', context)

def band_detail(request, id):
    band = get_object_or_404(Band, id=id)
    return render(request, 'band_detail.html', {'band': band})

# views.py
def venue_list(request):
    venues = Venue.objects.prefetch_related('room_set').all()
    return render(request, 'venue_list.html', {'venues': venues})