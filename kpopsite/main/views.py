from django.shortcuts import render
from news.models import News
from artists.models import MonthlyRating, Group, SoloArtist
from events.models import Event
from django.db.models import Max
from datetime import datetime
import json


def index(request):
    news = News.objects.all().order_by('-date_pub')[:8]

    latest_rating = MonthlyRating.objects.aggregate(
        latest_year=Max('annee'),
        latest_month=Max('mois')
    )

    latest_year = latest_rating['latest_year']
    latest_month = latest_rating['latest_month']

    boys_groups = MonthlyRating.objects.filter(
        artist_type='bg',
        annee=latest_year,
        mois=latest_month
    ).select_related('group').order_by('position')[:3]

    girls_groups = MonthlyRating.objects.filter(
        artist_type='gg',
        annee=latest_year,
        mois=latest_month
    ).select_related('group').order_by('position')[:3]

    events = Event.objects.all().select_related('group', 'solo_artist').order_by('date')

    artists_with_events = []

    groups_with_events = Group.objects.filter(
        group_events__isnull=False
    ).distinct()

    for group in groups_with_events:
        artists_with_events.append({
            'slug': group.slug,
            'name': group.name,
        })

    solos_with_events = SoloArtist.objects.filter(
        solo_events__isnull=False
    ).distinct()

    for solo in solos_with_events:
        artists_with_events.append({
            'slug': solo.slug,
            'name': solo.stage_name,
        })

    events_json = []
    for event in events:
        if event.group:
            artist_slug = event.group.slug
        elif event.solo_artist:
            artist_slug = event.solo_artist.slug
        else:
            artist_slug = 'none'

        events_json.append({
            'date': event.date.strftime('%Y-%m-%d'),
            'type': event.event_type,
            'title': event.title,
            'artist_slug': artist_slug
        })

    current_month = datetime.now().strftime('%B')
    current_year = datetime.now().year

    years = range(current_year - 2, current_year + 3)

    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }

    context = {
        'news': news,
        'boys_groups': boys_groups,
        'girls_groups': girls_groups,
        'latest_month': month_names.get(latest_month, ''),
        'latest_year': latest_year,
        'events': events,
        'artists_with_events': artists_with_events,
        'events_json': json.dumps(events_json),
        'current_month': current_month,
        'current_year': current_year,
        'years': years,
    }

    return render(request, 'main/index.html', context)


def about_us(request):
    return render(request, 'main/about_us.html')


def contact(request):
    return render(request, 'main/contact.html')


##########
# SEARCH #
##########

def search(request):
    query = ''
    content_type = ''
    artist_tags = []
    news_tags = []
    artists_results = []
    news_results = []
    no_results = False

    if request.method == 'GET' and request.GET.get('q'):
        query = request.GET.get('q', '').strip()
        content_type = request.GET.get('content_type', '')
        artist_tags = request.GET.getlist('artist_tags')
        news_tags = request.GET.getlist('news_tags')

        # Recherche artists
        if content_type != 'news':

            # Groupes
            groups = Group.objects.filter(name__icontains=query)

            # Vérification des tags
            if artist_tags:
                group_genders = []
                if 'male' in artist_tags:
                    group_genders.append('male')
                if 'female' in artist_tags:
                    group_genders.append('female')
                if 'mixed' in artist_tags:
                    group_genders.append('mixed')

                if group_genders:
                    groups = groups.filter(gender__in=group_genders)
                else:
                    groups = groups.none()

            # Groupes dans les resultats
            for group in groups:
                if group.gender == 'male':
                    gender_display = 'Boy Group'
                elif group.gender == 'female':
                    gender_display = 'Girl Group'
                else:
                    gender_display = 'Mixed Group'

                artists_results.append({
                    'type': 'group',
                    'name': group.name,
                    'slug': group.slug,
                    'photo': group.photo,
                    'gender_display': gender_display
                })

            # Solos
            soloists = SoloArtist.objects.filter(stage_name__icontains=query)

            # Vérification des tags
            if artist_tags:
                solo_genders = []
                if 'solo_m' in artist_tags:
                    solo_genders.append('m')
                if 'solo_f' in artist_tags:
                    solo_genders.append('f')

                if solo_genders:
                    soloists = soloists.filter(gender__in=solo_genders)
                else:
                    soloists = soloists.none()

            # Solos dans les resultats
            for artist in soloists:
                artists_results.append({
                    'type': 'solo',
                    'name': artist.stage_name,
                    'slug': artist.slug,
                    'photo': artist.photo,
                    'gender_display': 'Solo Artist'
                })

        # Recherche news
        if content_type != 'artists':
            news_results = News.objects.filter(title__icontains=query)

            # Vérification des tags
            if news_tags:
                news_results = news_results.filter(tag__in=news_tags)

            news_results = news_results.order_by('-date_pub')

        # Vérification pour les relustats vides
        if not artists_results and not news_results:
            no_results = True

    context = {
        'query': query,
        'content_type': content_type,
        'artist_tags': artist_tags,
        'news_tags': news_tags,
        'artists_results': artists_results,
        'news_results': news_results,
        'no_results': no_results,
    }

    return render(request, 'main/search.html', context)


#########
# GUIDE #
#########

def guide(request):
    return render(request, 'main/guide/guide.html')


def about_community(request):
    return render(request, 'main/guide/about_community.html')


def comebacks(request):
    return render(request, 'main/guide/comebacks.html')


def terms(request):
    return render(request, 'main/guide/terms.html')


def what_is_kpop(request):
    return render(request, 'main/guide/what_is_kpop.html')


def under_construction(request):
    return render(request, 'main/under_construction.html')