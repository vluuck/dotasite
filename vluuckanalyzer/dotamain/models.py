from django.db import models
from django.urls import reverse

# Create your models here.
class Match(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d", blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey("Category", on_delete=models.PROTECT, null=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})

    class Meta:
        verbose_name = "Матчі"
        verbose_name_plural = "Матчі"
        ordering = ["id"]

        

class Category(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name="Категорія")

    def __str__(self) -> str:
            return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name = "Категорії"
        verbose_name_plural = "Категорії"
        ordering = ["name"]


class Feedback(models.Model):
    email = models.EmailField(max_length=255)
    content = models.CharField(max_length=255)

    def __str__(self):
        return self.email + " " + self.content
    

    