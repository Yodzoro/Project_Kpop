from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.text import slugify  #au lieu d'id, l'URL affichera le titre (slug) et non les chiffres


# Fonctions pour les chemins d'accès dynamiques aux fichiers
def company_logo_path(instance, filename):
    # media/artists/companies/HYBE/hybe_logo.png
    return f'artists/companies/{instance.name}/{filename}'

def social_icon_path(instance, filename):
    # media/artists/social_icons/weverse.svg
    return f'artists/social_icons/{filename}'

def group_photo_path(instance, filename):
    # media/artists/boy_groups/BTS/bts_group.png
    if instance.gender == 'male':
        folder = 'boy_groups'
    elif instance.gender == 'female':
        folder = 'girl_groups'
    else:
        folder = 'mixed_groups'
    return f'artists/{folder}/{instance.name}/{filename}'


def group_logo_path(instance, filename):
    # media/artists/boy_groups/BTS/logos/bts_logo.png
    if instance.gender == 'male':
        folder = 'boy_groups'
    elif instance.gender == 'female':
        folder = 'girl_groups'
    else:
        folder = 'mixed_groups'
    return f'artists/{folder}/{instance.name}/logo/{filename}'


def member_photo_path(instance, filename):
    # media/artists/boy_groups/BTS/members/rm.png
    if instance.group:
        if instance.group.gender == 'male':
            folder = 'boy_groups'
        elif instance.group.gender == 'female':
            folder = 'girl_groups'
        else:
            folder = 'mixed_groups'
        return f'artists/{folder}/{instance.group.name}/members/{filename}'
    else:
        # Si le membre n'a pas de groupe
        return f'artists/solo/members/{filename}'


def solo_photo_path(instance, filename):
    # media/artists/solo_male/Taemin/taemin.png
    folder = 'solo_male' if instance.gender == 'm' else 'solo_female'
    return f'artists/{folder}/{instance.stage_name}/{filename}'


class Company(models.Model):
    logo = models.ImageField(upload_to=company_logo_path)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    date_fondation = models.DateField('Date de fondation')
    ceo = models.CharField(max_length=100)
    address = models.CharField(max_length=300)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Entreprise'
        verbose_name_plural = 'Entreprises'


class Member(models.Model):
    GENDER_CHOICES = [('m', 'male'), ('f', 'female')]

    photo = models.ImageField(upload_to=member_photo_path)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True, blank=True, related_name='group_members')
    stage_name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True, db_index=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_age = models.DateField('Date de naissance')
    nationality = models.CharField(max_length=100)
    birthplace = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    unit = models.CharField(max_length=100, blank=True, null=True)
    zodiac_sign = models.CharField(max_length=50)
    social_links = GenericRelation('SocialLink')
    fun_facts = models.TextField('Faits intéressants')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.stage_name)
            # Si le membre fait partie d'un groupe, ajouter le nom du groupe au slug.
            if self.group:
                self.slug = f"{base_slug}-{slugify(self.group.name)}"
            else:
                # Si c'est un solo/sans groupe, on utilise juste stage_name
                self.slug = base_slug

            # Vérification de l'unicité dans le modèle Member
            counter = 1
            original_slug = self.slug
            while Member.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.stage_name}' or f'{self.nom}'

    class Meta:
        verbose_name = 'Member'
        verbose_name_plural = 'Members'


class Group(models.Model):
    GENDER_CHOICES = [
        ('male', 'Boy Group'),
        ('female', 'Girl Group'),
        ('mixed', 'Mixed Group')
    ]

    photo = models.ImageField(upload_to=group_photo_path)
    logo = models.ImageField(upload_to=group_logo_path)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    name = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, null=True, db_index=True)
    fandom_name = models.CharField(max_length=100)
    date_debut = models.DateField('Date de début')
    slogan = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    social_links = GenericRelation('SocialLink')
    members = models.ManyToManyField(Member, related_name='member_groups')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = base_slug

            counter = 1
            while Group.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Groupe'
        verbose_name_plural = 'Groupes'


class SoloArtist(models.Model):
    GENDER_CHOICES = [('m', 'male'), ('f', 'female')]

    photo = models.ImageField(upload_to=solo_photo_path)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    stage_name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True, db_index=True)
    member = models.OneToOneField(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='solo_career')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_age = models.DateField('Date de naissance')
    nationality = models.CharField(max_length=100)
    birthplace = models.CharField(max_length=200)
    zodiac_sign = models.CharField(max_length=50)
    date_debut = models.DateField('Date de début')
    fandom_name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    social_links = GenericRelation('SocialLink')
    fun_facts = models.TextField('Faits intéressants')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.stage_name)
            self.slug = base_slug

            counter = 1
            while SoloArtist.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.stage_name}' or f'{self.nom}'

    class Meta:
        verbose_name = 'Solo Artiste'
        verbose_name_plural = 'Solo Artistes'

class MonthlyRating(models.Model):
    ARTIST_TYPE_CHOICES = [('bg', 'Boy group'), ('gg', 'Girl group')]

    artist_type = models.CharField(max_length=20, choices=ARTIST_TYPE_CHOICES)
    mois = models.PositiveIntegerField('Mois')
    annee = models.PositiveIntegerField('Année')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    position = models.PositiveIntegerField('Position', default=1)

    def __str__(self):
        group_name = self.group.name if self.group else 'No group'
        return f'{group_name} - {self.get_artist_type_display()} - {self.mois}/{self.annee} (#{self.position})'

    class Meta:
        verbose_name = 'Rating mensuelle'
        verbose_name_plural = 'Rating mensuelles'
        ordering = ['annee', 'mois', 'position']
        unique_together = [['artist_type', 'mois', 'annee', 'group']]

class SocialPlatform(models.Model):
    name = models.CharField('Nom', max_length=100, unique=True)  # sert aussi de texte pour l'infobulle
    icon = models.FileField(
        'Icône (SVG)',
        upload_to=social_icon_path,
        validators=[FileExtensionValidator(allowed_extensions=['svg'])],
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Plateforme sociale'
        verbose_name_plural = 'Plateformes sociales'
        ordering = ['name']


class SocialLink(models.Model):
    platform = models.ForeignKey(SocialPlatform, on_delete=models.CASCADE, related_name='links')
    url = models.URLField()

    # A quel objet appartient le lien (Group, Member ou SoloArtist)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.content_object} - {self.platform.name}'

    class Meta:
        verbose_name = 'Lien social'
        verbose_name_plural = 'Liens sociaux'
        ordering = ['id']
        indexes = [models.Index(fields=['content_type', 'object_id'])]