from django.db import models

class Author(models.Model):
    nickname = models.CharField(max_length=200)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='news/authors/', blank=True, null=True)

    def __str__(self):
        return f'{self.nickname}' or f'{self.nom} {self.prenom}'

    class Meta:
        verbose_name = 'Auteur'
        verbose_name_plural = 'Auteurs'

class News(models.Model):
    class Tags(models.TextChoices):
        BOY_GROUP = 'boy_group'
        GIRL_GROUP = 'girl_group'
        SOLO = 'solo'

    tag = models.CharField(max_length=20, choices=Tags.choices)
    cover = models.ImageField(upload_to="news/covers/")
    title = models.CharField(max_length=255)
    preview = models.CharField(max_length=250)
    full_text = models.TextField('Texte de l\'article')
    date_pub = models.DateTimeField('Date de publication')
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL) #Le site est petit, donc 1 auteur par article suffit

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'


