import re

from django import template
from django.urls import reverse
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from artists.models import Group, SoloArtist

register = template.Library()

# Syntaxe dans le texte de l'article :
#   [[group:kard|KARD]]       -> page du groupe (slug = kard)
#   [[solo:taemin|Taemin]]    -> page du soliste (slug = taemin)
LINK_RE = re.compile(r'\[\[(group|solo):([\w-]+)\|([^\[\]]+)\]\]')

# Noms des URL dans urls.py (à adapter si ils sont différents)
GROUP_URL = 'group_info'
SOLO_URL = 'solo_info'


def get_url(kind, slug):
    """Renvoie l'URL de la page, ou None si l'artiste n'existe pas."""
    if kind == 'group' and Group.objects.filter(slug=slug).exists():
        return reverse(GROUP_URL, args=[slug])

    if kind == 'solo' and SoloArtist.objects.filter(slug=slug).exists():
        return reverse(SOLO_URL, args=[slug])

    return None


@register.filter
def artist_links(text):
    """Transforme les marqueurs [[type:slug|texte]] en liens vers les pages des artistes."""
    escaped_text = conditional_escape(text)  # on échappe d'abord tout le texte (pas de HTML venant de la base)

    def replace(match):
        kind, slug, label = match.groups()
        url = get_url(kind, slug)
        if url is None:
            return label  # artiste introuvable : texte simple, sans lien (pas d'erreur 404 pour le lecteur)
        return f'<a href="{url}" class="article_artist_link">{label}</a>'

    return mark_safe(LINK_RE.sub(replace, escaped_text))