from django.shortcuts import render,get_object_or_404
from django.core.paginator import EmptyPage,Paginator,PageNotAnInteger
from .models import Listing
from listings.choices import price_choices,bedroom_choices,state_choices

def index(request):
    # listings = Listing.objects.all()
    listings = Listing.objects.order_by('-list_date').filter(is_publish=True)

    paginator = Paginator(listings,3)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    context = {
        'listings' : paged_listings
    }
    return render(request, 'listings/listings.html',context)

def listing(request,listing_id):
    listing = get_object_or_404(Listing,pk=listing_id)
    context = {
        'listing': listing
    }

    return render(request, 'listings/listing.html',context)

def search(request):
    queryset_listing = Listing.objects.order_by('-list_date')

    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_listing = queryset_listing.filter(description__icontains=keywords)

    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_listing = queryset_listing.filter(city__icontains=city)

    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_listing = queryset_listing.filter(state__iexact =state)

    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_listing = queryset_listing.filter(bedrooms__lte =bedrooms)

    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_listing = queryset_listing.filter(price__lte =price)

    context = {
        'price_choices': price_choices,
        'bedroom_choices': bedroom_choices,
        'state_choices': state_choices,
        'queryset_listing': queryset_listing,
        'values': request.GET,
    }
    return render(request, 'listings/search.html',context)

