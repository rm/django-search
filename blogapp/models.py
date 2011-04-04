from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, unique=True)

    def __unicode__(self):
        return u'%s <%s>' % (self.name, self.email)

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return u'%s' % self.name

class Entry(models.Model):
    author = models.ForeignKey(Author)
    date = models.DateTimeField()
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    text = models.TextField()
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return u'%s <%s> - %s' % (self.title, self.author.email, self.date)
