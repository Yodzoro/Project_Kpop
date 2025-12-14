from django.shortcuts import render, get_object_or_404
from artists.models import MonthlyRating, Group, SoloArtist
from django.db.models import Max
from collections import defaultdict


###########
# ARTISTS #
###########

def artists(request):
    boys_groups = Group.objects.filter(gender='male')[:4]
    girls_groups = Group.objects.filter(gender='female')[:4]
    mixed_groups = Group.objects.filter(gender='mixed')[:4]
    solo_male = SoloArtist.objects.filter(gender='m')[:4]
    solo_female = SoloArtist.objects.filter(gender='f')[:4]

    context = {
        'boys_groups': boys_groups,
        'girls_groups': girls_groups,
        'mixed_groups': mixed_groups,
        'solo_male': solo_male,
        'solo_female': solo_female,
    }

    return render(request, 'artists/artists_home.html', context)

"""
Grouper les artistes par première lettre
groups_by_letter - dict avec lettres comme clés
available_letters - liste des lettres avec artistes
"""
def groups_boys(request):
    boys_groups = Group.objects.filter(gender='male').order_by('name')

    groups_by_letter = defaultdict(list)
    available_letters = []

    for group in boys_groups:
        first_letter = group.name[0].upper()

        if first_letter.isalpha() and first_letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            groups_by_letter[first_letter].append(group)
            if first_letter not in available_letters:
                available_letters.append(first_letter)
        else:
            groups_by_letter['#'].append(group)
            if '#' not in available_letters:
                available_letters.append('#')

    groups_by_letter = dict(sorted(groups_by_letter.items()))
    available_letters.sort()
    if '#' in available_letters:
        available_letters.remove('#')
        available_letters.append('#')

    context = {
        'groups_by_letter': groups_by_letter,
        'available_letters': available_letters,
    }

    return render(request, 'artists/groupes/groups_boys.html', context)


def groups_girls(request):
    girls_groups = Group.objects.filter(gender='female').order_by('name')

    groups_by_letter = defaultdict(list)
    available_letters = []

    for group in girls_groups:
        first_letter = group.name[0].upper()

        if first_letter.isalpha() and first_letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            groups_by_letter[first_letter].append(group)
            if first_letter not in available_letters:
                available_letters.append(first_letter)
        else:
            groups_by_letter['#'].append(group)
            if '#' not in available_letters:
                available_letters.append('#')

    groups_by_letter = dict(sorted(groups_by_letter.items()))
    available_letters.sort()
    if '#' in available_letters:
        available_letters.remove('#')
        available_letters.append('#')

    context = {
        'groups_by_letter': groups_by_letter,
        'available_letters': available_letters,
    }

    return render(request, 'artists/groupes/groups_girls.html', context)


def groups_mix(request):
    mixed_groups = Group.objects.filter(gender='mixed').order_by('name')

    groups_by_letter = defaultdict(list)
    available_letters = []

    for group in mixed_groups:
        first_letter = group.name[0].upper()

        if first_letter.isalpha() and first_letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            groups_by_letter[first_letter].append(group)
            if first_letter not in available_letters:
                available_letters.append(first_letter)
        else:
            groups_by_letter['#'].append(group)
            if '#' not in available_letters:
                available_letters.append('#')

    groups_by_letter = dict(sorted(groups_by_letter.items()))
    available_letters.sort()
    if '#' in available_letters:
        available_letters.remove('#')
        available_letters.append('#')

    context = {
        'groups_by_letter': groups_by_letter,
        'available_letters': available_letters,
    }

    return render(request, 'artists/groupes/groups_mix.html', context)


def group_info(request, slug):
    group = Group.objects.get(slug=slug)

    members = group.members.all()

    context = {
        'group': group,
        'members': members,
    }
    return render(request, 'artists/groupes/group_info.html', context)


def solo_m(request):
    solo_male = SoloArtist.objects.filter(gender='m').order_by('stage_name')

    groups_by_letter = defaultdict(list)
    available_letters = []

    for artist in solo_male:
        first_letter = artist.stage_name[0].upper()

        if first_letter.isalpha() and first_letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            groups_by_letter[first_letter].append(artist)
            if first_letter not in available_letters:
                available_letters.append(first_letter)
        else:
            groups_by_letter['#'].append(artist)
            if '#' not in available_letters:
                available_letters.append('#')

    groups_by_letter = dict(sorted(groups_by_letter.items()))
    available_letters.sort()
    if '#' in available_letters:
        available_letters.remove('#')
        available_letters.append('#')

    context = {
        'groups_by_letter': groups_by_letter,
        'available_letters': available_letters,
    }

    return render(request, 'artists/solo/solo_male.html', context)


def solo_f(request):
    solo_female = SoloArtist.objects.filter(gender='f').order_by('stage_name')

    groups_by_letter = defaultdict(list)
    available_letters = []

    for artist in solo_female:
        first_letter = artist.stage_name[0].upper()

        if first_letter.isalpha() and first_letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            groups_by_letter[first_letter].append(artist)
            if first_letter not in available_letters:
                available_letters.append(first_letter)
        else:
            groups_by_letter['#'].append(artist)
            if '#' not in available_letters:
                available_letters.append('#')

    groups_by_letter = dict(sorted(groups_by_letter.items()))
    available_letters.sort()
    if '#' in available_letters:
        available_letters.remove('#')
        available_letters.append('#')

    context = {
        'groups_by_letter': groups_by_letter,
        'available_letters': available_letters,
    }

    return render(request, 'artists/solo/solo_female.html', context)


def solo_info(request, slug):
    artist = SoloArtist.objects.get(slug=slug)

    context = {
        'artist': artist,
    }
    return render(request, 'artists/solo/solo_info.html', context)


##########
# RATING #
##########

def rating(request):
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
    ).select_related('group').order_by('position')

    girls_groups = MonthlyRating.objects.filter(
        artist_type='gg',
        annee=latest_year,
        mois=latest_month
    ).select_related('group').order_by('position')

    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }

    context = {
        'boys_groups': boys_groups,
        'girls_groups': girls_groups,
        'latest_month': month_names.get(latest_month, ''),
        'latest_year': latest_year,
    }

    return render(request, 'artists/rating.html', context)