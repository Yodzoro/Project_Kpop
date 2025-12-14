from django.shortcuts import render
from news.models import News

"""
En raison du grand nombre de variables,
la variable context est utilisée pour améliorer la lisibilité.

Donc je ne utilise pas
return render(request, 'news/news_page.html', {'news': news, 'selected_tag': selected_tag, 'sort_order': sort_order,)

Mais
contexte = {
    'news': news,
    'selected_tag': selected_tag,
    'sort_order': sort_order,
}
return render(request, 'news/news_home.html', context)
"""

def news_home(request):
    news = News.objects.all()

    # Filtre par tag
    selected_tag = request.GET.get('tag', None)
    if selected_tag and selected_tag in ['boy_group', 'girl_group', 'solo']:
        news = news.filter(tag=selected_tag)

    # Filtre par date (par défaut(nouveau), plus ancien, plus récent)
    sort_order = request.GET.get('sort', 'latest')
    if sort_order == 'oldest':
        news = news.order_by('date_pub')
    else:
        news = news.order_by('-date_pub')

    context = {
        'news': news,
        'selected_tag': selected_tag,
        'sort_order': sort_order,
    }

    return render(request, 'news/news_home.html', context)


def news_page(request, id):
    article = News.objects.get(id=id)

    # On obtient les 3 dernières ([:3]) actualités (order_by('-date_pub')), à l'exception de celle en cours (exclude(id=id)).
    recommended_news = News.objects.exclude(id=id).order_by('-date_pub')[:3]

    context = {
        'article': article,
        'recommended_news': recommended_news,
    }

    return render(request, 'news/news_page.html', context)