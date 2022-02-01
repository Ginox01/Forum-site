from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from math import ceil

# Create your models here.


class Sezione(models.Model):
    nome = models.CharField(max_length=100)
    descrizione = models.CharField(max_length=500)
    immagine = models.ImageField()

    def __str__(self):
        return str(self.nome)

    def get_absolute_url(self):
        return reverse('section',kwargs={'pk':self.pk})

    def get_last_discussions(self):
        return Discussione.objects.filter(sezione_appartenenza=self).order_by("-data")[:3]

    def get_number_of_posts(self):
        return Post.objects.filter(discussione_appartenenza__sezione_appartenenza=self).count()

    def get_number_of_discussions(self):
        return Discussione.objects.filter(sezione_appartenenza=self).count()

    class Meta:
        verbose_name = 'Sezione'
        verbose_name_plural = 'Sezioni'

class Discussione(models.Model):
    sezione_appartenenza = models.ForeignKey(Sezione,on_delete=models.CASCADE,related_name='discussioni_appartenenza')
    titolo = models.CharField(max_length=100)
    primo_post = models.TextField()
    autore = models.ForeignKey(User,on_delete=models.CASCADE,related_name='discussioni')
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.titolo)

    def get_absolute_url(self):
        return reverse('discussion',kwargs={'pk':self.pk})

    def get_number_of_pages(self):
        numero_di_posts = Post.objects.filter(discussione_appartenenza=self).count()
        numero_di_pagine = ceil(numero_di_posts/5)
        return numero_di_pagine

    class Meta:
        verbose_name = 'Discussione'
        verbose_name_plural = 'Discussioni'

class Post(models.Model):
    discussione_appartenenza = models.ForeignKey(Discussione,on_delete=models.CASCADE,related_name='posts_appartenenza')
    autore = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    contenuto = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.autore)

