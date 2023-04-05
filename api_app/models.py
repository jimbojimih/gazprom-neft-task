from django.db import models
from django.contrib.postgres.fields import ArrayField
from pytils.translit import slugify


class Category(models.Model):
    title_category = models.CharField(max_length=300, )


class Quote(models.Model):
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ManyToManyField(Category, related_name='quotes')
    create_timestamp = models.DateTimeField()    
    timestamp = models.DateTimeField()
    language = models.CharField(max_length=50, )
    wiki = models.CharField(max_length=500, )
    title = models.CharField(max_length=500, )
    auxiliary_text = ArrayField(models.CharField(max_length=500, ), null=True)

    def get_absolute_url(self):
        return reverse ("article_detail",kwargs={'slug':self.slug})

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        i = 1
        while Quote.objects.filter(slug=unique_slug).exists():
            unique_slug = slug + str(i)
            i += 1
        return unique_slug        

    def save(self, flag=None, *args, **kwargs): 
        if flag != True:
            self.slug = self._get_unique_slug()        
        return super().save(*args, **kwargs)